# That module will pull all tracked stocke from the DB and run the prediction model

from pymongo import MongoClient
from logger import logger
from datetime import datetime, timedelta
from env import env
from model_trainning.nn_model import  model_train_api
import requests
from logger import logger
from flask import Blueprint
import json
import os 

model_generation_module = Blueprint(env.route_model_train, __name__)
# Pull all tracked stock from buy_signal_track collection

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)
db = client[env.DB_NAME]
collection = db[env.COLLECTION_NAME_STOCKS_UNDER_TRACKING]

@model_generation_module.route(env.route_model_train, methods=['POST'])
def pull_tracked_stock():
    """
    Pull all tracked stock from the buy_signal_track collection in the stock_predict database.

    :return: The cursor object of the tracked stock
    :rtype: pymongo.cursor.Cursor
    """

    tracked_stock = collection.find()
    list_tracked = list(tracked_stock)
    logger.info(f"DATA PROCESSOR: Data processor started")
    for stock in list_tracked:
        stock_title = stock[env.STOCK_TITLE_FILED_NAME]
        logger.info(f"DATA PROCESSOR:Stock title: {stock_title} sent for training")
        tracking_data_14_days = stock[env.TRACKING_FIELD_NAME_14_DAYS]
        print("stock title:", stock_title)
        print("tracking data 14 days:", tracking_data_14_days)
        json_data = {
            "stock_title": stock_title
        }
        response = requests.post(env.base_url + env.route_nn_training_model, json = json_data)
        response = requests.post(env.base_url + env.route_lstm_training_model, json = json_data)
        logger.info(f"DATA PROCESSOR:Response from model trainer : {response.text}")
        logger.info(f"DATA PROCESSOR:*************************************************")
    return {"status": "success"}, 200


# http://127.0.0.1:5000/model-prepare