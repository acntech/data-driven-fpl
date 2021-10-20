"""Convert data to CSV."""

from pathlib import Path


def _get_game_week(data: dict) -> int:
    """Get the gameweek from a data dump.

    Args:
        data (dict): data dict.
    Returns:
        int: Current gameweek
    """
    gameweek = list(filter(lambda x: x["is_current"] is True, data["events"]))

    return gameweek[0]["id"] if gameweek else 0


def json_to_csv(data_dir: str, entity: str):
    """Convert multiple JSON into csv.

    Args:
        data_dir (str): Path to dir holding JSON dumps of Fantasy Premier League.
        entity (str): Either "elements" or "teams".
    """

    # Getting all .json files from data_dir
    data_dir = Path(data_dir)
    files = sorted([file for file in data_dir.iterdir() if file.suffix == ".json"])

    # Creating path to interrim file
    interim_path = Path("data", "interim", data_dir.name + "_" + entity)
    interim_path = interim_path.with_suffix(".csv")
    interim_path.parent.mkdir(exist_ok=True)

    # TODO: Fill in logic that can be described with the following pseudocode:
    #
    # for each file in files
    #   open file and load json
    #   for each element in entity
    #       append download_time and gameweek
    #   write the enity to CSV
    #
    # Useful functions are:
    #  1. open() -> https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files
    #  2. json.load() -> https://docs.python.org/3/library/json.html
    #  3. map() ->
    #  https://realpython.com/python-map-function/#using-map-with-different-kinds-of-functions
    #  4. Pandas.DataFrame.to_csv ->
    #  https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
