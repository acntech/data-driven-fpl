"""Transformations module."""

import pandas as pd


def calculate_diff(df_grouped: pd.core.frame.DataFrame, columns: list):
    """Calculate the difference between cumulative columns on gameweek level.

    Args:
        df_grouped (pd.core.frame.DataFrame): DF that contains at least "code" and "gameweek"
        columns (list): Columns to calculate diff on.

    Returns:
        pd.core.frame.DataFrame: Dataframe with diff calculated in place.
    """
    try:
        columns.remove("code")
    except ValueError:
        pass

    df_g = df_grouped.groupby(by=["code", "gameweek"], as_index=False).last()
    df_g.loc[df_g.gameweek != 0, columns] = (
        df_g[df_g.gameweek != 0][columns.copy() + ["code"]].groupby(by="code").diff().fillna(df_g)
    )
    return df_g


def add_target_value(dataframe, target="minutes", window=5):
    """Add a target value ahead in time.

    Args:
        df (pandas.DataFrame): grouped elements or teams df
        target (str, optional): Name of variable to create target from
        window (int, optional): Number of future records to generate target from
    Returns:
        df: df with appended target column
    """
    dataframe.loc[::-1, "target"] = (
        dataframe.iloc[::-1]
        .groupby("code")[target]
        .apply(lambda x: x.rolling(min_periods=1, window=window).sum().shift(1))
    )
    return dataframe


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
