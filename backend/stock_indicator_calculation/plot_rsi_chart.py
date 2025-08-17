import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
matplotlib.use('Agg')
def plot_rsi(df: pd.DataFrame, close_price_column :str = 'Close',rsi_column: str = 'RSI', title: str = 'RSI Indicator'):
    """
    Plot RSI with overbought and oversold levels.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing RSI data.
    rsi_column : str
        Name of the column containing RSI values.
    title : str
        Title of the plot.
    """
    df.to_csv('rsi_data.csv')

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # --- Price subplot ---
    ax1.plot(df.index, 'Close', label='Close Price', color='orange')
    ax1.set_title(f'{title} - Close Price')
    ax1.set_ylabel('Price')
    ax1.grid(True)
    ax1.legend(loc='upper left')

    # --- RSI subplot ---
    ax2.plot(df.index, df[rsi_column], label='RSI', color='blue')
    ax2.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    ax2.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    ax2.axhline(50, color='gray', linestyle='--', alpha=0.5)

    ax2.set_title(f'{title} - RSI')
    ax2.set_ylabel('RSI')
    ax2.set_ylim(0, 100)
    ax2.grid(True)
    ax2.legend(loc='upper left')

    plt.xlabel('Date')
    plt.tight_layout()
    print("Save chart")
    plt.savefig('rsi_chart.png')