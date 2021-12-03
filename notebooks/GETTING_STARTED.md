---
jupyter:
  jupytext:
    formats: md,ipynb
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

# Todays task 📝

Todays task focus on getting to understand our dataset. We want to identify what data could be useful for our machine learning model. We also want to get a deeper understanding of the dataset - at least the variables identified as interesting. Todays task consist of:

1. Select the variables that YOU think will be useful for our machine learning model
2. Dig deep in the selected variables and fill out metadata for each one using the provided data_desc.json

```javascript
IPython.OutputArea.auto_scroll_threshold = 10;
```

```python
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_columns", None)
pd.set_option('display.max_rows', 100)
```

## Somewhere to keep our notes

For practical purposes we store our findings in JSON file. We can load this file as a dict and update it with our findings! Notebooks are great - but lets store our findings a in a both useful, persistant and readable format.

The json can be updated both programatically (see example below) or directly through VSCode.

#### Structure of our notes
```json
{
    elements: {
        "code": {
            "description": # Describe the function of the variable
            "type":  # continuous discrete ordinal nominal other
            "dtype": # string integer float boolean datetime
            "calculated": # snapshot cumulative_sum static average percentage ratio
            "action": # keep drop engineer
            "notes": # Your personal notes
        }
    },
    teams: {...}
    fixtures: {...}
}
```


### Example of updating notes programatically

We utilize the python builtin JSON package -> https://docs.python.org/3/library/json.html

```python
# We load our JSON-file as a dict - we can now update it with our finding!
with open("../data_desc/data_desc.json") as file:
    data_desc = json.load(file)
```

```python
# To add information we can use .update()
data_desc["elements"]["code"].update({
    "description": "Unique identifier for each player",
    "type": "nominal",
    "dtype": "integer",
    "calculated": "static",
    "action": "keep"})

# Or assign a value directly
data_desc["elements"]["code"]["notes"] = "What is the difference between code and id?"
data_desc["elements"]["code"]
```

```python
# We save our notes back to our json.
with open("../data_desc/data_desc.json", "w") as file:
    json.dump(data_desc, file, indent=4, ensure_ascii=False)
```

## Loading our data

We start by loading our newly converted CSVs for teams and elements. We also wanna have a look at what fixtures are all about.

We know/guess that:
* elements - holds information about FPL players i.e Mohammed Salah, Harry Kane etc.
* teams - holds information about each team represented in the current FPL season.
* fixtures - holds information about all the matches.

Lets load our data!

```python
# Loading our CSV into a Pandas Dataframe
elements_2020_df = pd.read_csv("../data/interim/2020-fpl-data_elements.csv")
#teams_2020_df = pd.read_csv("../data/interim/2020-fpl-data_teams.csv")

# We also grab one dump of fixtures
#with open("../data/raw/2020-fpl-fixtures/2020-09-14T00-00-00Z_data.json") as file:
#    fixtures = json.load(file)
#    fixtures_2020_df = pd.DataFrame(fixtures["fixtures"])
```

# Now it is your turn 🎓

Some tips on the way!
1. There is a massive amount of data - both variables and records. Try utilize groupby to reduce the data size using pandas.GroupBy --> https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html
2. Try to identify variables that contribute the most to explaining your target variable.
    * One tips is to use Seaborn to visualize the [correlation matrix](https://seaborn.pydata.org/examples/many_pairwise_correlations.html#plotting-a-diagonal-correlation-matrix).
    * Feature engineering is _not_ the a part of this task - however we might need to utilize _some_ engineering to find a useful target variable. For example we can add a future value of a player. See the provided ```add_target_value``` function.
3. Try to understand the data and ask yourself:
    * What is the purpose of the variable?
    * What type of variable is it? -> https://builtin.com/data-science/data-types-statistics
    * How is the variable measured/recorded?

```python
def add_target_value(df, target="minutes", window=5, is_cumsum=False):
    """Add a target value ahead in time.

    Args:
        df (pandas.DataFrame): grouped elements or teams df
        target (str, optional): Name of variable to create target from
        window (int, optional): Number of future records to generate target from
        is_cumsum (bool, optional): If the column is cumulative we need to shift a little to make any sense.
    Returns:
        df: df with appended target column
    """
    if is_cumsum:
        # We make sure that the starting point _this_ season is 0
        df.loc[df.gameweek == 0, target] = 0

        # We calculate the difference between each record
        df["temp"] = df.groupby(by="code", as_index=False)[target].diff()
    else:
        df["temp"] = df[target]
    df.loc[::-1, "target"] = df.iloc[::-1].groupby('code')["temp"].apply(lambda x: x.rolling(min_periods=1, window=window).sum().shift(1))
    df = df.drop(["temp"], axis=1)
    return df

# An example where we look at how future minutes

# We first group our dataframe on "code" and gameweek and select the last record each gameweek for each player.
elements_2020_grouped = elements_2020_df.groupby(by=["code", "gameweek"], as_index=False).last()

# We calculcate our target value and look if it makes sense for one player.
add_target_value(elements_2020_grouped, target="minutes", window=2, is_cumsum=True)[elements_2020_grouped.web_name=="Salah"]
```

```python

```
