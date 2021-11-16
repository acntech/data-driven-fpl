"""Convert data to CSV."""
import json
from pathlib import Path
from tqdm import tqdm
import pandas as pd


class DataConverter:
    """Data converter class."""

    def __init__(
        self, data_dir: str, entity: str, main_data_folder="data", main_interim_folder="interim"
    ):
        """Set configuration parameters.

        Args:
            data_dir (str): Path to dir holding JSON dumps of Fantasy Premier League.
            entity (str): Either "elements" or "teams".
        """
        self.data_dir = Path(data_dir)
        self.entity = entity
        self.interim_folder_path = Path(main_data_folder, main_interim_folder)
        self.interim_folder_entity_path = Path(
            self.interim_folder_path, self.data_dir.name + "_" + self.entity
        ).with_suffix(".csv")

    def make_interim_folder_if_absent(self):
        """Generate interim folder if non-existant.
        """
        self.interim_folder_entity_path.parent.mkdir(exist_ok=True)

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

        files = sorted([file for file in self.data_dir.iterdir() if file.suffix == ".json"])

        self.make_interim_folder_if_absent()

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
                    self.interim_folder_entity_path,
                    mode="w" if i == 0 else "a",
                    index=False,
                    header=(i == 0),
                )

            except TypeError:
                print(f"Something is wrong in file {path}")
            except json.JSONDecodeError:
                print(f"Something is wrong with JSON formatting in file {path}")
