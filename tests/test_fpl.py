"""Demonstrate test."""
from fpl import __version__


def test_version():
    """Assert version of application."""
    assert __version__ == "0.1.0"
