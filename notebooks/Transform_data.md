---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.2
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import pandas as pd
import time
from tqdm import tqdm
from fpl.transform.transformations import calculate_diff
```

```python
# Decorators, what are they? -> realpython.com/primer-on-python-decorators/
def timer(func):
    def wrapper_timer(*args, **kwargs):
        # Do something before the function:
        start = time.time()

        # Execute the original function.
        temp = func(*args, **kwargs)

        # Exectute something after the function
        print(f"Execution of {func.__name__} took {time.time() - start}")
        return temp
    # Return the function wrapped.
    return wrapper_timer

@timer
def get_data(*args, **kwargs):
    return pd.read_parquet(*args, **kwargs)
```

```python
# Illustrate speed difference between different reads
read_csv = timer(pd.read_csv)
df_csv = read_csv("../data/interim/2021-fpl-data_elements.csv")
df_all = get_data("../data/interim/2021_elements_parquet/")
df_selected = get_data("../data/interim/2021_elements_parquet/", columns=["code", "gameweek", "minutes", "event_points"])
df_filtered = get_data("../data/interim/2021_elements_parquet/", filters=[('code', '=', 98747)])
```

```python
# Illustrate memory difference between different reads
print(f"Whole dataframe: {df_csv.memory_usage().sum()//10**6} mb")
print(f"Whole dataframe: {df_all.memory_usage().sum()//10**6} mb")
print(f"Selected columns: {df_selected.memory_usage().sum()//10**6} mb")
print(f"Filtered columns: {df_filtered.memory_usage().sum()//10**6} mb")
```

```python
@timer
def transform_dataset(path_to_parquet, codes=None, teams_df=None):
    if not codes:
        codes = pd.read_parquet(path_to_parquet, columns=["code"], partitioning=["team_code", "code"])
    for i, code in enumerate(tqdm(df_selected["code"].unique())):
        df = pd.read_parquet(path_to_parquet, filters=[('code', '=', 98747)], partitioning=["team_code","code"])
        df_g = df.groupby(by=["code", "gameweek"], as_index=False).last()
        # Before transformation
        df_g.loc[:, "minutes"] = calculate_diff(df_g["minutes"])
        df_g = join_elements_and_team(df_g, teams_df)
        # After transformation
```

```python
@timer
def join_elements_and_team(elements_df, teams_df):
    elements_df = elements_df.groupby(by=["code", "gameweek"], as_index=False).last()
    teams_df = teams_df.groupby(by=["code", "gameweek"], as_index=False).last()
    return elements_df.join(teams_df.set_index(["code", "gameweek"]), on=["team_code", "gameweek"], rsuffix="_team")

```

```python
teams_df = get_data("../data/interim/2021_teams_parquet/")
```

```python

```
