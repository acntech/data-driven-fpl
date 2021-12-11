"""Test transformations."""
import pytest

from fpl.transform.transformations import add_target_value, calculate_diff, join_elements_and_team


def test_calculate_diff(elements_df):
    """Test fpl.transform.transformations.calculate_diff."""
    elements_df_g = elements_df.groupby(by=["code", "season", "gameweek"], as_index=False).last()
    diff = calculate_diff(elements_df_g, ["minutes"])

    # Check that minutes are never over 2 * 90 minutes
    assert (diff[diff.gameweek != 0]["minutes"] <= 270).all()

    # Check that the returned series matches 0-38 gameweeks
    assert len(diff) == 36


def test_join_elements_and_team(elements_df, teams_df):
    """Test fpl.transform.transformations.join_elements_and_team."""
    elements_df = elements_df.groupby(by=["code", "gameweek"], as_index=False).last()
    test_df = join_elements_and_team(elements_df=elements_df, teams_df=teams_df)

    # Assert that num elements has not changed
    assert len(test_df) == 36

    # Assert that teams columns are added
    assert len(test_df.columns) == 91


@pytest.mark.parametrize("row_n, window_size, target", [(0, 5, 48), (1, 2, 8)])
def test_add_target_value(elements_df, row_n, window_size, target):
    """Test the fpl.transform.tranformation.add_target_value."""
    elements_df = elements_df.groupby(by=["code", "season", "gameweek"]).last()
    elements_df = add_target_value(elements_df, "event_points", window=window_size)

    assert "target" in elements_df.columns.tolist()
    assert elements_df["target"].iloc[row_n] == float(target)
    assert elements_df["event_points"].iloc[1 + row_n : 1 + row_n + window_size].sum() == target
