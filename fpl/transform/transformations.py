"""Transformations module."""


def calculate_diff(series):
    """Return the diff for a cumuliative column.

    Args:
        series (pandas.core.series.Series): Series to calculate diff on.

    Returns:
        pandas.core.series.Series: Series that diff is calculated on.
    """
    series.iloc[1:] = series.iloc[1:].diff().fillna(series.iloc[1:])
    return series.copy()
