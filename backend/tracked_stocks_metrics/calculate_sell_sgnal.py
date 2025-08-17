from pymongo import MongoClient
import pandas as pd 
import json
import ast
import os

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client['stock_predict']
collection_stock_data = db['sp500_stocks_data']


def calculate_sell_signal(stock_title: str):
    print("claculating sell signal........................................")
    sell_signal_result = {}
    stock_data = collection_stock_data.find_one({"stock_title": stock_title})
    data_frame = stock_data.get('data_frame')
    try:
        data_frame_list = ast.literal_eval(data_frame)
    except Exception as e:
        print(f"Error: {str(e)}")
        print("failed", type(data_frame))
        print(f"Error decoding datafrane data for stock {stock_title}")
        return
    # print("Data frame for sell signal:",type(data_frame_list))
    # Create a DataFrame from the stock data
    try:
        stock_df: pd.DataFrame = pd.DataFrame(data_frame_list)
    except:
        print(f"Error decoding datafrane data for stock {stock_title}")
        return
    
    # print("Data frame for sell signal:",stock_df)
    # Calculate 14 days RSI 
    delta = stock_df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    stock_df['RSI'] = 100 - (100 / (1 + rs))

    # Calculate 20-day simple moving average
    stock_df['MA20'] = stock_df['Close'].rolling(window=20).mean()

    # Create SELL flag
    stock_df['SELL'] = (stock_df['RSI'] > 70) & (stock_df['Close'] < stock_df['MA20'])
    # print(stock_df.tail(20))
    # Get last row
    last_row = stock_df.iloc[-1]
    
    # print("Last Date:", last_row['Date'])
    # print("Close:", round(last_row['Close'], 2))
    # print("RSI:", round(last_row['RSI'], 2))
    # print("MA20:", round(last_row['MA20'], 2))
    # print("SELL Signal:", bool(last_row['SELL']))

    
    # print("SELL signal found")
    sell_signal_result['date'] = last_row['Date']
    sell_signal_result['sell_signal'] = bool(last_row['SELL'])
    sell_signal_result['close_price'] = round(last_row['Close'], 2)
    sell_signal_result['rsi'] = round(last_row['RSI'], 2)
    sell_signal_result['ma20'] = round(last_row['MA20'], 2)
    return sell_signal_result