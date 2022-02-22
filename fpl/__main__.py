"""The main module."""
from fpl import __version__
from fpl.cli import data, pipe, root


def start_script():
    """Demo only."""
    root.add_command(data)
    root.add_command(pipe)
    root()


if __name__ == "__main__":
    root()
