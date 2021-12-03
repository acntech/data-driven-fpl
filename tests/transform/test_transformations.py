"""Test transformations."""
from fpl.transform.transformations import calculate_diff, join_elements_and_team


def test_calculate_diff(elements_df):
    """Test calculate diff."""
    elements_df_g = elements_df.groupby(by=["code", "gameweek"]).last()
    salah = elements_df_g.loc[elements_df_g.web_name == "Salah"]
    diff = calculate_diff(salah["minutes"]).tolist()

    # Check that minutes are never over 2 * 90 minutes
    for minutes in diff[1:]:
        assert minutes <= 180
    # Check that the returned series matches 0-38 gameweeks
    assert len(diff) == 39


def test_join_elements_and_team(elements_df, teams_df):
    """Test the join transformation."""
    elements_df = elements_df.groupby(by=["code", "gameweek"], as_index=False).last()
    test_df = join_elements_and_team(elements_df=elements_df, teams_df=teams_df)

    # Assert that num elements has not changed
    assert len(test_df) == 78

    # Assert that teams columns are added
    assert len(test_df.columns) == 90
