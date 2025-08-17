"""
This module is responsible for collecting data from the `buy_signal` collection in Mongo and storing it in the `buy_signal_track` collection.
It will also append new data to existing items in the collection.
"""
from flask import Flask, jsonify, request, Blueprint
from pymongo import MongoClient
from datetime import datetime
from env import env 
from logger import logger
import os 


collection_buy_signal_store_module  = Blueprint(env.route_collect_buy_signal, __name__)

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)
db = client['stock_predict']
collection = db['buy_signal_track']
collection_stock_data = db['sp500_stocks_data']

@collection_buy_signal_store_module.route(env.route_collect_buy_signal,  methods=['POST','GET'])
def buy_data_collection():
    """
    This function is the entry point for the `buy_signal` collection data.
    It will receive data from the `buy_signal` collection in Mongo and store it in the `buy_signal_track` collection.
    If the stock is not under tracking, it will create a new item in the collection.
    If the stock is under tracking, it will append new data to the existing item in the collection.
    """
    # logger.info(f"{env.collect_buy_signal_name}: Collecter recivied data for tracking")
    from collect_buy_signal_stock import check_missed_days 
    print("hit collector")
    try:
        # Get the data from the request body
        stock_buy_signal =  request.get_json()
    except Exception as e:
        print("Failed for:",e)
        logger.error(f"{env.collect_buy_signal_name}: Failed to recive data for tracking")
        return {"status":"failed"}
   
    # Get the stock title from the data
    stock_title = stock_buy_signal.get('stock_title')
    
    # Get the last date the data was pulled from the data
    last_date_day_pull = stock_buy_signal.get('last_day_date')
    last_date_day_pull_datetime = datetime.strptime(last_date_day_pull , "%Y-%m-%d")   
    # Get the closing price of the stock from the data
    closing_price = stock_buy_signal.get('last_closing_price')
    # get buy signal 
    buy_signal = stock_buy_signal.get('last_buy_signal').get('signal')
    
    # Check if the stock is under tracking
    if stock_buy_signal.get('under_tracking') == 0:
        # Stock is not unrder tracking, first time stock will be added
        collected_buy_signal_stock_data = { 
            # Set the stock title
            "stock_title": stock_title,
            # Set the first buy signal data
            "first_buy_signal_data": last_date_day_pull_datetime,
            # Set the 14 days tracking data
            "days_tracking": [{"date": last_date_day_pull_datetime, "closing_price": closing_price, "predicted_price": False}],
            # buy signal value 
            "buy_signal": buy_signal,
            # Set the next day predictions data
            "next_day_predictions": [],
            # Price when flagged as buy signal
            "buy_signal_price": closing_price
            }
        try:
            # Insert the data into the collection
            collection.insert_one(collected_buy_signal_stock_data)
        except Exception as e:
            print("Failed to store data in MongoDB:",e)
            logger.error(f"{env.collect_buy_signal_name}: Failed to store data in MongoDB")
            return {"status":"failed"}
        logger.info(f"{env.collect_buy_signal_name}: {stock_title} not under tracking and has buy signal.. start tracking")
        return {"status":"new buy signal stored"} 
    else:
        # Implement append to existing item data
        logger.info(f"{env.collect_buy_signal_name}: {stock_title} is under tracking and will add next data to existing item")
        print("stock is under tracking, should be append to existing item in DB")
        # Create a query to find the item in the collection
        query = {"stock_title": stock_title}
        
        # Create a new stock value
        new_stock_value = {"date": last_date_day_pull_datetime, "closing_price": closing_price, "predicted_price": False}
        
        # Verification new value date is older than iexisting one 
        pipeline = [
                    {"$match": query},
                    {"$project": {"last_item": {"$arrayElemAt": ["$days_tracking", -1]}}}
                ]
        result = list(collection.aggregate(pipeline))
        if len(result) == 0:
            logger.error(f"{env.collect_buy_signal_name}: {stock_title} is not in DB")
            return {"status":"failed"}
        last_item_date = result[0].get("last_item")
        if last_item_date is None:
            logger.error(f"{env.collect_buy_signal_name}: {stock_title} is in DB but last item is None")
            return {"status":"failed"}
        # Get the existing date from the last item
        existing_date = last_item_date["date"]
        # Define the new item's date
        new_date = datetime.strptime(last_date_day_pull, "%Y-%m-%d")
        print(f"exisiting last stock - {stock_title} date in Mongo:", existing_date)
        print("New value date:", new_date)
        if new_date > existing_date: 
            try:
                # Update the data in the collection
                update_result = collection.update_one(query, {"$push": {"days_tracking": new_stock_value}})
                print("Updated result:", update_result.modified_count)
            except Exception as e:
                print("Failed to update data in MongoDB:",e)
                logger.error(f"{env.collect_buy_signal_name}: Failed to update data in MongoDB")
                return {"status":"failed"}
            logger.info(f"{env.collect_buy_signal_name}: {stock_title} , date: {last_item_date} is under tracking and will add next data to existing item")
        else:
            print("new value date is same or lower then existing")
            logger.info(f"{env.collect_buy_signal_name}: {stock_title} - new data is not relevant due old date")
            
        # check if some dates are missing 
        check_missed_days.check_and_fill_missed_days(stock_title)
        return {"status":"append"}

