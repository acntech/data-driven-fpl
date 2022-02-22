[![codecov](https://codecov.io/gh/acntech/data-driven-fpl/branch/main/graph/badge.svg?token=VLY920KXJV)](https://codecov.io/gh/acntech/data-driven-fpl)
[![Run pre-commit and publish coverage](https://github.com/acntech/data-driven-fpl/actions/workflows/lint-and-test-pipeline.yml/badge.svg?branch=main)](https://github.com/acntech/data-driven-fpl/actions/workflows/lint-and-test-pipeline.yml)
# **The data-driven FPL miniproject**
[**Table of content**](#the-data-driven-fpl-miniproject)
- [**The data-driven FPL miniproject**](#the-data-driven-fpl-miniproject)
  - [**The mission objective 🎯**](#the-mission-objective-)
  - [**Waypoint 1: Getting started**](#waypoint-1-getting-started)
    - [Tasks](#tasks)
    - [Resources:](#resources)

## **The mission objective 🎯**
Throughout Q1 and Q2 of FY22 we will iterate on a mini-project on a fantasy-football dataset. The project will force creative thinking and smart solutions. There are no right answers so please keep and open and exploratory mind.

Our objective can be summerized with the following:

* Create a solution to guide and support novice _FPL-players_ to make better in-game decisions.
* Learn approaches to data science, machine learning and python development
* Have fun with the group and get creative with the task at hand.


## **Waypoint 1: Getting started**
GOAL: Create a python-repo and download data!

### Tasks
1. Structure a python repo that ensures:
    * No data is checked into version control
    * Prevents unformatted code to be pushed to remote
2. Add required dependencies/requirements
3. Download data to local machine
    * Create a script that downloads only new data to local machine

### Resources:
* [A data driven repo by Cookie cutter template](https://drivendata.github.io/cookiecutter-data-science/#contributing)
* [Pre-commit](https://pre-commit.com/)
* [Poetry for python](https://python-poetry.org/)
* [Azure blob storage quickstart](https://docs.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme?view=azure-python)

```python
# To connect to data storage
STORAGE_ACCOUNT_URL= "https://martinfplstats1337.blob.core.windows.net/"
FPL_2020_CONTAINER= "2020-fpl-data"
FPL_2021_CONTAINER = "2021-fpl-data"
```

## **Waypoint 2: Looking at our data**
Goal: Understand our dataset to select useful data for machine learning.
### **Tasks**
#### **Part 1. - Converting our data to CSV**
This part focus on python and how to extract data from our downloaded blobs. Great opportunity for hands-on python. Start this part by checking either one of:
```bash
git checkout wp-2-startpoint-minimal
git checkout wp-2-startpoint-anine
```
1. Create a function that extract either "teams" or "elements" from all .JSON files in a directory and store the resulting table as a .CSV file.
    * Write the function in ```fpl/data/data_converter_class.py```
    * Each record in the table must be appended with ```gameweek``` and ```download_time```. The function to extract value for current gameweek is provided.
    * The CSV-file must be saved in ```data/interim/YYYY-fpl-data_entity.csv```. For example a csv-table of _elements_ from ```data/raw/2020-fpl-data``` should be stored as ```data/interim/2020-fpl-data_elements.csv```
2. Utilize [Click](https://www.palletsprojects.com/p/click/) to create an interface to run our convertion functions from the CLI
    * You should be able to:
        * Specify which entity to extract from the JSON files
        * The directory to fetch .JSON files from
    * Write your code in ```fpl/cli.py```

#### **Part 2. - Understanding our data**
This part focus on data understanding. Skip straight to this part to check out eihter
```bash
git checkout wp-2-startpoint-minimal-data
git checkout wp-2-startpoint-anine-data
```
1. Given your understanding of Fantasy football, use the available data to propose one or more ways machine learning can be utilized to provide enhance in-game decisions.
    * What are you going to predict?
    * How will this help fantasy football participants?
2. Select data that could be useful for a machine learning model.
    * Use Jupyter and the notebook ```notebooks/GETTING_STARTED.md``` to analyze variables found in:
        * teams
        * elements
        * fixtures
    * Select and describe the variables you find most important
    * Store the results in ```data_desc/data_desc.json```


## **Waypoint 3: Transforming our dataset**
This waypoint is all about transforming and wrangling our dataset. However - due to the size of the dataset we need to be smart about how we work with the data. As of now the dataset _do_ fit in memory. But with a evergrowing dataset this might change. The data also needs to be prepared for macchine learning - and we need to make use of learnt lessons from the previous waypoint to ready the dataset for learning.

**Todays goal is the following:**

* Explore different ways to transform our dataset to make it ready for machine learning
* Understand how to work with a "large" dataset without loading all of it into memory.

**Get started by checking out the code!**
```bash
git checkout wp-3-start # No help
git checkout wp-3-transform # Converting to parquet is done for you!
git checkout wp-3-solution # I just wanna look at a minimum solution.
```



### **Tasks**
#### **Part 1. - Splitting up the dataset and store as parquet.**
This task consist of converting our dataset to a more managable format - parquet. Parquet is nice because
it:
* Allows for quicker read speeds
* Allows to load only parts of the dataset when needed.

We are going to work with [```pandas```](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) and [```pyarrow```](https://arrow.apache.org/docs/python/dataset.html) to convert our dataset. To complete this task do the following:

1. Implement a function in [```fpl/data/make_parquet.py```](fpl/data/make_parquet.py) that
    1. reads a csv from disk to memory chunk by chunk.
    2. Each chunk is written to a parquet dataset before the next chunk is loaded
    3. Has a smart partitioning of the parquet dataset to optimize for read speed in the transformation step.
2. Write a nice cli entry point to invoke tranformation to parquet in [```fpl/cli.py```](fpl/cli.py) that:
    1. Lets users specify input csv file. Default value ```data/interim/raw_elements.csv```
    2. Lets users  specify output of parquet. Default value ```data/interim/elements_parquet```
    3. Lets user specify partition columns.
    4. Exits the program if a parquet dataset already exist, can be overridden by passing ```--force```
3. Implement tests to test:
    1. converting csv to parquet
    2. invoking the CLI without triggering the "csv to parquet" function.

#### **Part 2. - Transforming our dataset**
This task consists of transforming the dataset to a shape that can be used with a machine learning model. Considerations to make are:
* What do you want to predict?
* What kind of machine learning model do you see fit for this problem?

_A suggestion is to look at a machine learning model that tries to predict future ```event_points``` and look at data on a ```gameweek``` level._

**In short this task requires that:**

1. Decide on which columns (for starters) to proceed with and do transformations on.
   1. The recommended are marked in [```data_desc/data_desc.json```](data_desc/data_desc.json) with either ```keep``` or ```engineer```.  **Feel free to include more**
2. In the file [```fpl/transform/transformations.py```](fpl/transform/transformations.py) implement methods to transform the data.
   1. We need at least a function to handle columns with cumulative values (like ```minutes```)
   2. We need a function that adds a target value (future ```event_points```) is a candidate.
   3. We need a way to join ```elements``` data with ```teams``` data.
3. Sow everything together in a jupyter notebook.


## **Waypoint 3: Setting up an input pipeline for our dataset**
