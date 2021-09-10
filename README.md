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