"""Test utils."""
import pytest

from fpl.utils.helpers import timer


def test_timer(capsys):
    """Test timer-wrapper."""

    def mock_function():
        startpoint = 0
        for i in range(10):
            startpoint += i ** 2

    func = timer(mock_function)
    func()
    captured = capsys.readouterr()
    assert "Execution of mock_function took" in captured.out

    func(print_time=False)
    captured = capsys.readouterr()
    assert not captured.out


@pytest.mark.parametrize(
    "print_time, input, expected_result, expected_output",
    [(True, 0, 45, True), (False, 1, 46, False)],
)
def test_timer_pie_notation(capsys, print_time, input, expected_result, expected_output):
    """Test pie notation of timer.

    Checks that adding wrapper does not interfere with function logic.
    """

    @timer
    def mock_function(num, startpoint=0):
        for i in range(num):
            startpoint += i
        return startpoint

    assert mock_function(10, print_time=print_time, startpoint=input) == expected_result
    captured = capsys.readouterr()
    assert ("Execution of mock_function took" in captured.out) is expected_output
