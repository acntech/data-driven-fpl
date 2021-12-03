"""Convert data to CSV."""
import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from fpl.utils import paths


class DataConverter:
    """Data converter class."""

    def __init__(self, entity: str, raw_data_path=None, interim_data_path=None):
        """Set configuration parameters.

        Args:
            entity (str): Either "elements" or "teams".
            raw_data_path (Path, optional): Path to dir holding JSON dumps of raw data.
            interim_data_path (Path, optional): Path to dir for uploading converted data.
        """
        self.entity = entity
        if raw_data_path is None:
            raw_data_path = paths.get_raw_data_path()
        self.__raw_data_path = Path(raw_data_path)
        if interim_data_path is None:
            interim_data_path = paths.get_interim_data_path()
        self.__interim_data_path = Path(interim_data_path)
        self._interim_data_entity_path = Path(
            self.__interim_data_path, self.__raw_data_path.name + "_" + self.entity
        ).with_suffix(".csv")

    def _make_interim_folder_if_absent(self):
        """Generate interim folder if non-existant."""
        self._interim_data_entity_path.parent.mkdir(exist_ok=True)

    def _get_game_week(self, data: dict) -> int:
        """Get the gameweek from an events list.

        Args:
            data (dict): data dict.
        Returns:
            int: Current gameweek
        """
        gameweek = list(filter(lambda x: x["is_current"] is True, data["events"]))

        return gameweek[0]["id"] if gameweek else 0

    def convert_json_to_csv_on_entity(self):
        """Convert multiple JSON into csv according to selected entity.

        Args:
            data_dir (str): Path to dir holding JSON dumps of Fantasy Premier League.
            entity (str): Either "elements" or "teams".
        """

        files = sorted([file for file in self.__raw_data_path.iterdir() if file.suffix == ".json"])

        self._make_interim_folder_if_absent()

        for i, path in enumerate(tqdm(files, desc="Loading CSV")):
            try:
                with open(path, encoding="utf-8") as file:
                    data = json.load(file)
                    gameweek = self._get_game_week(data)
                    list(
                        map(
                            lambda x, data=data, gameweek=gameweek: x.update(
                                {"download_time": data["download_time"], "gameweek": gameweek}
                            ),
                            data[self.entity],
                        )
                    )
                dataframe = pd.DataFrame(data[self.entity])
                dataframe.to_csv(
                    self._interim_data_entity_path,
                    mode="w" if i == 0 else "a",
                    index=False,
                    header=(i == 0),
                )

            except TypeError as e:
                print(f"Something is wrong in file {path}:", e)
            except json.JSONDecodeError:
                print(f"Something is wrong with JSON formatting in file {path}")
