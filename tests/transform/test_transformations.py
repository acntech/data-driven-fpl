"""Test transformations."""
from fpl.transform.transformations import calculate_diff, join_elements_and_team


def test_calculate_diff(elements_df):
    """Test calculate diff."""
    elements_df_g = elements_df.groupby(by=["code", "gameweek"], as_index=False).last()
    diff = calculate_diff(elements_df_g, ["minutes"])

    # Check that minutes are never over 2 * 90 minutes
    assert (diff[diff.gameweek != 0]["minutes"] <= 270).all()

    # Check that the returned series matches 0-38 gameweeks
    assert len(diff) == 78


def test_join_elements_and_team(elements_df, teams_df):
    """Test the join transformation."""
    elements_df = elements_df.groupby(by=["code", "gameweek"], as_index=False).last()
    test_df = join_elements_and_team(elements_df=elements_df, teams_df=teams_df)

    # Assert that num elements has not changed
    assert len(test_df) == 78

    # Assert that teams columns are added
    assert len(test_df.columns) == 90
