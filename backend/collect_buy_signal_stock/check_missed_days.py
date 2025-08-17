from pymongo import MongoClient
import pandas as pd
import json
from datetime import datetime
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import logger

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)


db = client['stock_predict']
collection_buy_signal = db['buy_signal_track']
collection_stock_data = db['sp500_stocks_data']

def check_and_fill_missed_days(stock_title:str) -> int:
    """
    Function check if tracking data has missing dates and fill them
    Args:
        stock_title (str): _description_
    Returns: bool
    """
    
    print("Checking missed days for:", stock_title)
    logger.info(f"Checking missed days for: {stock_title}")
    # Pulling data from stock data and stock tracking collection 
    stock_data = collection_stock_data.find_one({"stock_title": stock_title})
    track_data_doc = collection_buy_signal.find_one({"stock_title": stock_title})

    # Buy signal date 
    buy_signal_date =  track_data_doc['first_buy_signal_data']

    # Loading data table with last year data
    stock_data_df = pd.DataFrame(json.loads(stock_data['data_frame']))
    stock_data_df['Date'] = pd.to_datetime(stock_data_df['Date'])
    # Filtering all rows after buy signal date
    dates_after_buy_signal_date = stock_data_df[stock_data_df['Date'] >= buy_signal_date]

    # Loading tracked dates 
    track_data_dates = track_data_doc['days_tracking']
    tracked_dates = [date['date'] for date in track_data_dates]

    # filter rows where not tracked dates 
    missed_tracked_dates = dates_after_buy_signal_date[~dates_after_buy_signal_date['Date'].isin(tracked_dates)]
    print(f"Found {len(missed_tracked_dates)} missed dates for stock {stock_title}")
    logger.info(f"Found {len(missed_tracked_dates)} missed dates for stock {stock_title}")
    for index, row in missed_tracked_dates.iterrows():
        # Preparing data prior append 
        last_date_day_pull_datetime = row['Date']
        closing_price = row['Close']
        # Dict to appedn 
        new_stock_value = {"date": last_date_day_pull_datetime, "closing_price": closing_price, "predicted_price": False}

        print(f"Adding {new_stock_value} to {stock_title} in buy signal track")
        track_data_dates.append(new_stock_value)
        track_data_dates.sort(key=lambda x: x['date'])
        print("New tracked list", track_data_dates)
        update_result = collection_buy_signal.update_one({"_id": track_data_doc['_id']}, {"$set": {"days_tracking": track_data_dates}})
        print("Updated result:", update_result.modified_count)
        print(f"Updated result: {update_result.modified_count} for stock {stock_title} with value {new_stock_value}")
    print("missed dates:", missed_tracked_dates)

# if __name__ == "__main__":
#     check_and_fill_missed_days("ADBE")