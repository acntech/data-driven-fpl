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

## Now its your turn! Fill in logic to transform the dataset :-)

```python
@timer
def transform_dataset():
    pass
```

```python

```
