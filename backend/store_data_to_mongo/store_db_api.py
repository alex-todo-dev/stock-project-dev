
from flask import Flask, jsonify, request, Blueprint, url_for
from pymongo import MongoClient
import requests
from env import env
from logger import logger
import os 


store_stock_data_to_mongo_module  = Blueprint(env.route_store_data_mongo, __name__)

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client['stock_predict']
collection = db['sp500_stocks_data']
collection_stocks_under_tracking = db['buy_signal_track']


@store_stock_data_to_mongo_module.route(env.route_store_data_mongo, methods=['POST'])
def trend_calculation_store_to_db():
    """
    Endpoint to store stock data and handle buy signal tracking.

    Logs the data sending event, stores the data, checks if the stock is under tracking,
    evaluates buy signal, and potentially sends data to a buy signal collector.

    Returns:
        dict: A dictionary containing the status of the operation.
    """
    # Log the initiation of data storage
    logger.info(f"{env.store_data_mongo_name}: data sent to Store_to_mongo module")

    from store_data_to_mongo import store_data_to_mongo

    # Retrieve and copy the JSON data from the request
    data = request.get_json()
    data_for_store = data.copy()

    # Store the data in the database 
    status = store_data_to_mongo.store_data(data_for_store)
    print(status)

    # Initialize under_tracking flag
    data['under_tracking'] = 0

    # Retrieve list of stocks under tracking from the database
    stocks_under_tracking = list(collection_stocks_under_tracking.find())
    stocks_names_under_tracking_list = [stock_name.get('stock_title') for stock_name in stocks_under_tracking]

    # Check if the stock is already under tracking
    if stocks_names_under_tracking_list:
        if data.get('stock_title') in stocks_names_under_tracking_list:
            data['under_tracking'] = 1
            logger.info(f"{env.store_data_mongo_name}: stock already under tracking")

    # Retrieve buy signal
    buy_signal = data.get('last_buy_signal').get('signal')
    print("BUY SIGNAL:", buy_signal)
    print("Under tracking:", data['under_tracking'])

    # If buy signal is active or stock is under tracking, send data to collector
    if buy_signal != 0 or data['under_tracking']:
        logger.info(f"{env.store_data_mongo_name}: {data.get('stock_title')} ,stock under tracking {data.get('under_tracking')} or buy signal = {buy_signal} ")
        response_from_buy_signal_collect = requests.post(env.base_url + env.route_collect_buy_signal, json=data)
        print("response from collector:", response_from_buy_signal_collect)
        logger.info(f"{env.store_data_mongo_name}: Data sent to collector, response from collector {response_from_buy_signal_collect}")
    else:
        logger.info(f"{env.store_data_mongo_name}: {data.get('stock_title')} ,stock under tracking {data.get('under_tracking')} or buy signal = {buy_signal} ")

    return {"status": "data_stored_for:" + data['stock_title']}
