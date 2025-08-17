"""
Module calculates the moving average for a given stock data.
"""

from env import env


def calculate_moving_average(stock_data, window=env.MOVING_AVERAGE_WINDOW_SIZE):
    """
    Calculate the moving average for a given stock data.

    Parameters
    ----------
    stock_data : DataFrame
        DataFrame containing the stock data.
    window : int, optional
        Size of the window for calculating the moving average. Default is
        `MOVING_AVERAGE_WINDOW_SIZE`.

    Returns
    -------
    DataFrame
        DataFrame with the calculated moving average.
    """
    # Calculate the moving average
    stock_data['SMA'] = stock_data['Close'].rolling(window=window).mean()

    # Calculate the absolute difference between the closing price and the moving
    # average
    stock_data['Absolute_MA'] = stock_data['Close'] - stock_data['SMA']

    # Drop rows with NaN values
    stock_data = stock_data.dropna()

    return stock_data
