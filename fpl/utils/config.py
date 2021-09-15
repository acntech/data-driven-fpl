"""Methods to parse config files."""
import yaml


def get_config(config_file_path):
    """Convert config yaml file to dictionary.

    Args:
        config_file_path : Path
            Path to config directory.

    Returns:
        config : dict
            Config represented as dictionary.
    """
    with open(config_file_path) as data:
        config = yaml.load(data, Loader=yaml.FullLoader)
    return config
