---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
from tqdm import tqdm
from fpl.transform.transformations import calculate_diff, join_elements_and_team, add_target_value
from fpl.data.make_parquet import write_df_to_dataset, get_parquet
from fpl.utils.helpers import timer
import pandas as pd
from pathlib import Path
import shutil
import json
```

# Load our data

We have now the same dataset saved as both ```.csv``` and ```.parquet```. We load our dataset in different ways just _to demo_ speed to load the data.

Observe that parquet allows you to:
* Load just a few columns of the dataset
* Filter the dataset based on a value in a column

For more detailed descriptions of pyarrow and parquet datasets: https://arrow.apache.org/docs/python/dataset.html

```python
FPL_DATA_ELEMENTS_2020_CSV = "../data/interim/raw_elements.csv"
FPL_DATA_ELEMENTS_2020_PARQUET = "../data/interim/elements_parquet/"
FPL_DATA_TEAMS_2020_PARQUET = "../data/interim/teams_parquet/"
PROCESSED_2020_DATASET = "../data/processed/fpl-dataset/"
```

```python
# Illustrate speed difference between different reads
read_csv = timer(pd.read_csv)
df_csv = read_csv(FPL_DATA_ELEMENTS_2020_CSV)
df_all = get_parquet(FPL_DATA_ELEMENTS_2020_PARQUET)
df_selected = get_parquet(FPL_DATA_ELEMENTS_2020_PARQUET, columns=["code", "gameweek", "minutes", "web_name", "event_points"])
df_filtered = get_parquet(FPL_DATA_ELEMENTS_2020_PARQUET, filter=('code',98747))
```

```python
# Illustrate memory difference between different reads
print(f"Whole dataframe: {df_csv.memory_usage().sum()//10**6}mb")
print(f"Whole dataframe: {df_all.memory_usage().sum()//10**6}mb")
print(f"Selected columns: {df_selected.memory_usage().sum()//10**6}mb")
print(f"Filtered columns: {df_filtered.memory_usage().sum()//10**6}mb")
```

<!-- #region -->
### WTF? Why is df_all smaller than df_csv other?

Turns out that columns that are partitioned on are stored in the "filestructure" of parquet when using ```"hive"``` as partitioning flavor. Observe a print of the dataset structure.

```bash
data/interim/2020_elements_parquet
├── team_code=1
├── team_code=11
├── team_code=13
................
................
```

When the dataset is loaded back into the DF the datatype changes from ```int64``` to ```int32```. The memory saved for this alone account from the 3 mb
<!-- #endregion -->

```python
# The mysterious 3mb
print(f"df_csv[\"team_code\"] dtype: {df_csv.team_code.dtype} memory usage {df_csv.team_code.memory_usage()//10**6}mb")
print(f"df_all[\"team_code\"] dtype: {df_all.team_code.dtype} memory usage {df_all.team_code.memory_usage()//10**6}mb")
```

# Transform the data

To transform the data we:
* Load "logical" subsets of the dataset to save memory
* Apply our transformations
* Append the subset to a new dataset in "processed"

Expressed as pseudocode we do:

```
for all elements from a particular team in parquet dataset
    apply transformations
    add transformed players to new parquet file in new dataset
```



### Lets apply our transformations!

We load our dataset metadata and "choose" columns that we decided to "keep" or "engineer". Lets print those columns to see what we are going to work with!

```python
with open("../data_desc/data_desc.json") as file:
    data_desc = json.load(file)

# Nested list comprehension syntax is complex: https://realpython.com/list-comprehension-python/#watch-out-for-nested-comprehensions
chosen_columns = {key: item for _, x in data_desc.items() if isinstance(x, dict) for key, item in x.items() if item["action"] in ["keep", "engineer"]}
chosen_columns.keys()
```



### Lets apply our transformations!

We load our dataset metadata and "choose" columns that we decided to "keep" or "engineer". Lets print those columns to see what we are going to work with!

```python
@timer
def transform_dataset(elements_path, teams_path, output_path, columns_to_keep=None):
    # We add "target" to columns to keep.
    if columns_to_keep:
        columns_to_write = set(list(columns_to_keep.keys()) + ["target"])

    # We remove any old transformed dataset
    if Path(output_path).is_dir():
        shutil.rmtree(output_path)
    teams = get_parquet(elements_path, columns=["team_code"])["team_code"].unique().tolist()
    for team in teams:
        elements_df = get_parquet(elements_path, filter=('team_code', team), print_time=False).groupby(by=["code", "season", "gameweek"], as_index=False).last()
        teams_df = get_parquet(teams_path, filter=('code', team), print_time=False).groupby(by=["code", "season", "gameweek"], as_index=False).last()

        # Apply transformations

        # Handle gw 0
        elements_df.loc[elements_df.gameweek == 0, ["minutes", "total_points", "ict_index"]] = elements_df[elements_df.gameweek == 0][["minutes", "total_points", "ict_index"]] // 38

        # Calculate the value scored for each gameweek instead of the total sum.
        elements_df = calculate_diff(elements_df, ["code", "minutes", "total_points", "ict_index"])

        # Put minutes into bins.
        elements_df["minutes"] = pd.cut(elements_df["minutes"], bins=[0,1,30,60,90,180, float("inf")], include_lowest=True, labels=False)

        # Join data from the "teams" dataset
        elements_df = join_elements_and_team(elements_df, teams_df)

        # Add our target value
        elements_df = add_target_value(elements_df, "total_points")

        # Write the transformed DF to dataset.
        if not columns_to_keep:
            columns_to_write = elements_df.columns.tolist() + ["season"]


        write_df_to_dataset(elements_df[columns_to_write], output_path, partition_columns=["team_code"], print_time=False)
```

```python
transform_dataset(FPL_DATA_ELEMENTS_2020_PARQUET, FPL_DATA_TEAMS_2020_PARQUET, PROCESSED_2020_DATASET, columns_to_keep=chosen_columns)
```

## Control that transformations have been executed as planned

```python
processed_df = get_parquet(PROCESSED_2020_DATASET)
salah = processed_df[processed_df.web_name == "Salah"]
salah.head(60)
```

```python
# Check that the event_points 5 gameweeks into the future equals target
assert salah.event_points[1:6].sum() == int(salah.target.iloc[0]), "Sum of n next points are not equal to target"

# Assert that all minutes, except in GW 0 are in the range 0-180 minutes
assert ((salah.minutes[1:] <= 180) & (salah.minutes[1:] >= 0)).all(), "Some minutes are more than expected 180 min"

# Assert event_points == total_points after diff
assert salah.event_points[1:-1].equals(salah.total_points[1:-1].astype(int)), "Event_points do not equal diffed total_points"


```

### Strange event_points != total_points when diffed

Observe that it seems that event_points are not the same as (total_points n +1) - (total_points n) in weeks that the player plays more than 90 min (so-called double gameweeks)

We might argue that for our case (as long as we look at the data from a gameweek level) the target value should in fact be the diffed total_points and not event_points
