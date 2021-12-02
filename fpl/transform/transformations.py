"""Transformations module."""


def calculate_diff(series):
    """Return the diff for a cumuliative column.

    Args:
        series (pandas.core.series.Series): Series to calculate diff on.

    Returns:
        pandas.core.series.Series: Series that diff is calculated on.
    """
    series = series.copy()
    series.iloc[1:] = series.iloc[1:].diff().fillna(series.iloc[1:])
    return series


def join_elements_and_team(elements_df, teams_df):
    """Join elements and teams df.

    Args:
        elements_df (pandas.core.frame.DataFrame): Grouped elements dataframe
        teams_df (pandas.core.frame.DataFrame): Grouped teams_dataframe

    Returns:
        pandas.core.frame.DataFrame: Return the joined dataframe.
    """
    elements_df = elements_df.groupby(by=["code", "gameweek"], as_index=False).last()
    teams_df = teams_df.groupby(by=["code", "gameweek"], as_index=False).last()
    return elements_df.join(
        teams_df.set_index(["code", "gameweek"]), on=["team_code", "gameweek"], rsuffix="_team"
    )
