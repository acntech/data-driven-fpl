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
    * Write the function in ```fpl/data/convert_data.py```
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