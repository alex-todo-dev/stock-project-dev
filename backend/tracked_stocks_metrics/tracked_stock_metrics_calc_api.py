
from flask import Flask, jsonify, request, Blueprint, url_for
from pymongo import MongoClient
import requests
from env import env
from logger import logger
import os


tracked_stocks_metrics_module  = Blueprint(env.route_tracked_stocks_metrics, __name__)

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client['stock_predict']
collection_stock_data = db['sp500_stocks_data']
collection_stocks_under_tracking = db['buy_signal_track']
collection_stock_metrics = db['tracked_stock_metrics']


@tracked_stocks_metrics_module.route(env.route_tracked_stocks_metrics, methods=['GET'])
def stock_metrics_clalculation():
    from .calculate_error import error_calculation
    from .trend_calculation import trend_calculation
    from .calculate_sell_sgnal import calculate_sell_signal

    print('stock_metrics_clalculation started')
    try:
        tracked_stocks = collection_stocks_under_tracking.find({},{'_id': 0})
        tracked_stocks_list = list(tracked_stocks)
    except Exception as e:
        print("Fialed to pull data from mongo:", e)
        return {'status': 'failed'}
    for stock in tracked_stocks_list:
        metric_data = {}
        stock_title = stock.get('stock_title')
        # dlete old data 
        delete_old_data_count = collection_stock_metrics.delete_many({'stock_title': stock_title})
        print("Deleted old data count:",delete_old_data_count)
        # Claluclation error real vs predicted price
        prediction_error = error_calculation(stock)
        print(prediction_error)
        # Trend calculation up or down
        trend = trend_calculation(stock)
        print(trend)
        # Calculate sell signal
        sell_signal = calculate_sell_signal(stock_title)
        print("Sell signal:", sell_signal)
        metric_data['stock_title'] = stock_title
        metric_data['prediction_error'] = prediction_error
        metric_data['trend'] = trend
        metric_data['sell_signal'] = sell_signal
        collection_stock_metrics.insert_one(metric_data)
    return {'status': 'metrics calculated'}