def generate_buy_signal(df):
    """
    Generate buy signals based on RSI and SMA.

    Parameters
    ----------
    df : DataFrame
        Must contain 'RSI', 'SMA', and 'Close' columns.

    Returns
    -------
    DataFrame
        Updated with 'Buy_signal' column.
    """
    df = df.copy()
    df['Buy_signal'] = 0


#     Level	Conditions
# 0	No signal
# 1	RSI < 40 (regardless of SMA)
# 2	RSI < 40 and Close > SMA
# 3	RSI < 30 and Close > SMA (strongest buy signal)

    # Strongest buy signal
    df.loc[(df['RSI'] < 30) & (df['Close'] > df['SMA']), 'Buy_signal'] = 3

    # Medium buy signal
    df.loc[(df['RSI'] < 40) & (df['Close'] > df['SMA']), 'Buy_signal'] = 2

    # Weak buy signal (RSI < 40 regardless of SMA)
    df.loc[(df['RSI'] < 40), 'Buy_signal'] = 1

    return df


