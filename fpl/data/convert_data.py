"""Convert data to CSV."""

import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm


def _get_game_week(data: dict) -> int:
    """Get the gameweek from a events list.

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
    data_dir = Path(data_dir)
    files = sorted([file for file in data_dir.iterdir() if file.suffix == ".json"])

    # Creating path to interim file
    interim_path = Path("data", "interim", data_dir.name + "_" + entity)
    interim_path = interim_path.with_suffix(".csv")
    interim_path.parent.mkdir(exist_ok=True)
    for i, path in enumerate(tqdm(files, desc="Loading CSV")):
        try:
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
                gameweek = _get_game_week(data)
                list(
                    map(
                        lambda x, data=data, gameweek=gameweek: x.update(
                            {
                                "download_time": data["download_time"],
                                "gameweek": gameweek,
                            }
                        ),
                        data[entity],
                    )
                )
            dataframe = pd.DataFrame(data[entity])
            dataframe.to_csv(
                interim_path, mode="w" if i == 0 else "a", index=False, header=(i == 0)
            )

        except TypeError:
            print(f"Something is wrong in file {path}")
        except json.JSONDecodeError:
            print(f"Something is wrong with JSON formatting in file {path}")
