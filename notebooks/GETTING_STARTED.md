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
teams_2020_df = pd.read_csv("../data/interim/2020-fpl-data_teams.csv")

# We also grab one dump of fixtures
with open("../data/raw/2020-fpl-fixtures/2020-09-12T10-24-34Z.json") as file:
    fixtures = json.load(file)
    fixtures_2020_df = pd.DataFrame(fixtures["fixtures"])
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
add_target_value(elements_2020_grouped, target="event_points", window=2, is_cumsum=False)[elements_2020_grouped.web_name=="Salah"]
```

## There are no right and wrong answers here.
There are no right or wrong answers here.


### Columns to drop!
Are there any columns that we should not care about from the get-go?

```python
def is_na(df, entity):
    # Update all columns that contain only NaN to {action:"drop"}
    for column in df.columns[df.isna().all()].tolist():
        data_desc[entity][column].update({"action": "drop"})

is_na(elements_2020_df, "elements")
is_na(teams_2020_df, "teams")
is_na(fixtures_2020_df, "fixtures")

# We inspect team!
data_desc["teams"]
```

### Dtypes are almost for free!
We fill out our dtypes as they might help us with further understanding/filtering

```python
# Lets populate data_desc with something that we know - data types (int, float, string, etc.)
def _fix_dtype_name(name):
    """Return name of pandas dtype."""
    if name == "int64":
        return "integer"
    elif name == "float64":
        return "float"
    elif name == "object":
        return "string"
    elif name == "bool":
        return "boolean"
    else:
        return name

def _check_float(column):
    """Check if column in fact is float."""
    try:
        if column.fillna(0).apply(lambda x: x % 1 == 0).all():
            return "integer"
        return "float"
    except TypeError:
        return None

def update_dtypes(df, entity):
    for column in df.columns:
        dtype = _fix_dtype_name(df[column].dtype.name)
        if dtype == "float":
            dtype = _check_float(df[column])
        data_desc[entity][column].update({"dtype": dtype})

# We update our data_desc with data types
update_dtypes(elements_2020_df, "elements")
update_dtypes(teams_2020_df, "teams")
update_dtypes(fixtures_2020_df, "fixtures")

# We then inspect total_points from elements
data_desc["elements"]["total_points"]
```

```python
# We find the number unique values for every variable in our dataset and store it in a separete df.
# We also filter out columns we dont care about, either those we decided to drop or already have a type!
# We could flip the filter and only look at columns we want to keep.

def _filter(df, entity):
    return df[[key for key, element in data_desc[entity].items() if element["type"] == None and element["action"] != "drop"]]

unique_values = _filter(elements_2020_df.nunique(), "elements")
```

## Looking for interesting variables

Since the amount of variables is massive we have a look at variables that correlate with our selected target variable. In this case we have chosen to try to predict future event_points.

Lets have a look!

```python
# We add a target variable which is the total event_points that a player gets in the upcomming N gameweeks.
elements_2020_grouped = add_target_value(elements_2020_grouped, "event_points", window=2)
```

```python
# We then calculate the correlation of elements and sort based on which variables correlate with our target
corr = elements_2020_grouped[[key for key, data in data_desc["elements"].items() if data["action"] != "drop" and data["dtype"] not in ["string", "boolean"]]+ ["target"]].corr()
corr.sort_values(by="target")["target"]
```

```python
# We can also display the correlation matrix!
import numpy as np

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(22, 18))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1., center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
```

### There are some serious correlations here!
Let at least keep some of the variables no matter what. Those are candidates to start to investigate in detail!

```python
# We store the most promising variables in keep and update
keep = corr[(corr["target"] > 0.30) | (corr["target"] < -0.30)]["target"].index.tolist()
keep.pop() #aaaand remember to remove target

# Then update our data_desc
for variable in keep:
    data_desc["elements"][variable]["action"] = "keep"


```

## Looking for nominal variables

We try to identify nominal (categorical) variables in our data set. Things to look for:
1. Variables with a limited number of unique values
2. Variables that are categorical but not ranked
3. Unique identifiers are considered nominal

```python
# We update our data_description with our findings
nominal_columns = [
    "code",
    "element_type",
    "first_name",
    "id",
    "in_dreamteam",
    "second_name",
    "special",
    "status",
    "team",
    "team_code",
    "web_name"]

for column in nominal_columns:
    data_desc["elements"][column].update({"type": "nominal"})
```

## Looking for ordinal variables

This time we look for categorical columns that are ranked. Things to look for:
1. Variables with the same number of unique values as a unique identifier (ie. same or close to as "code")
2. Usually integers, but can be strings (HIGH, MEDIUM LOW)
4. If rank or order is in the variable name its a tell 😉

```python
ordinal_columns = [
    "chance_of_playing_next_round",
    "chance_of_playing_this_round",
    "corners_and_indirect_freekicks_order",
    "direct_freekicks_order",
    "penalties_order",
    "threat_rank",
    "influence_rank",
    "creativity_rank",
    "threat_rank",
    "ict_index_rank",
    "influence_rank_type",
     "creativity_rank_type",
     "threat_rank_type",
     "ict_index_rank_type",
     "gameweek",
     "download_time"
]

for column in ordinal_columns:
    data_desc["elements"][column].update({"type": "ordinal"})
```

### Looking for discrete variables

We now look for discrete variables. These are numerical variables that seems to be a count of some sort.
We can look for:

1. Values that seems to be counted
2. Values that with dtype integear and cannot be divided into smaller pieces.

```python
discrete_columns = [
    "cost_change_event",
    "cost_change_event_fall",
    "cost_change_start",
    "cost_change_start_fall",
    "dreamteam_count",
    "event_points",
    "now_cost",
    "total_points",
    "transfers_in",
    "transfers_in_event",
    "transfers_out",
    "transfers_out_event",
    "minutes",
    "goals_scored",
    "assists",
    "clean_sheets",
    "goals_conceded",
    "own_goals",
    "penalties_saved",
    "penalties_missed",
    "yellow_cards",
    "red_cards",
    "saves",
    "bonus",
    "bps",

]
for column in discrete_columns:
    data_desc["elements"][column].update({"type": "discrete"})
```

### Looking for continuous variables
We look for data that we can not count, only measure!
Look out for:

* Variables that can hold an unlimited amount of different values
* Variables with dtype float could be a tell
* Interval data (i.e temperature)
    * No true zero
* Ratio data (i.e height)
    * Has a true zero


```python
continuous_columns = ["ep_next",
                      "ep_this",
                      "form",
                      "points_per_game",
                      "selected_by_percent",
                      "value_form",
                      "value_season",
                      "influence",
                      "creativity",
                      "threat",
                      "ict_index",
]
for column in continuous_columns:
    data_desc["elements"][column].update({"type": "continuous"})
```

## Identifying how data is calculated

One thing to look for is assumptions of how the data is measured/updated/calculated. In this section we try to understand how our data are measured. Are we looking at:

* Snapshot (either as gameweek or download-time as time point)
* Cumulative sum (untill now this season)
* Averages
* Fractions, percentage or some sort of ratio

There is no easy way of doing this other than:
1. Ask the SME/domain expert.
2. Investigate the data
3. Guess!

```python
# We can inspect a variable in detail and observe change over time.
elements_2020_grouped[elements_2020_grouped.web_name == "Salah"]["value_form"]
```

```python
# Here is a visualization of the same. Include more players if needed.
sns.lineplot(data=elements_2020_grouped[elements_2020_grouped.web_name.isin(["Salah", "Werner"]) ], x="gameweek", y="value_form")
```

```python
# We save our notes back to our json.
with open("../data_desc/data_desc.json", "w") as file:
    json.dump(data_desc, file, indent=4, ensure_ascii=False)
```
