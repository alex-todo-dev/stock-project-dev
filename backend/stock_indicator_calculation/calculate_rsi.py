import pandas as pd
import numpy as np
from env import env

def calculate_rsi(
    df: pd.DataFrame,
    column: str = env.COLUMN_CALCULATION_NAME_RSI,
    period: int = env.RSI_WINDOW_SIZE,
    output_column: str = 'RSI',
) -> pd.DataFrame:
    
    """
    Calculate Relative Strength Index (RSI) for the given DataFrame using Wilder's method.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the stock data.
    column : str, optional
        Column name for the data. Default is 'Close'.
    period : int, optional
        Window size for RSI calculation. Default is 14.
    output_column : str, optional
        Name of the output column. Default is 'RSI'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with an additional RSI column.
    """
    # from .plot_rsi_chart import plot_rsi
    delta = df[column].diff()

    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    # Use Wilder’s smoothing method (exponential weighted moving average)
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df[output_column] = rsi
    # plot_rsi(df, output_column)
    return df