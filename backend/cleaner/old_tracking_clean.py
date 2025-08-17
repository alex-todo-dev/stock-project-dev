"""
Clean old tracked data from DB and delete old model files
"""
from pymongo import MongoClient
from logger import logger
from datetime import datetime, timedelta
from env import env
from flask import Blueprint
from cleaner.model_delete_func import delete_model_files
import os
clean_module = Blueprint(env.route_cleaner_module, __name__)


@clean_module.route(env.route_cleaner_module, methods=['POST'])
def clean_old_tracking() -> dict:
    """
    Clean old tracked data from DB and delete old model files

    Returns:
        dict: A dictionary containing the status of the operation.
    """
    logger.info(f"{env.cleaner_module_name}: Start cleaning old tracked data from DB")

    # Fetch Mongo URI from environment variable, fallback to localhost
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    # Create MongoDB client
    client = MongoClient(mongo_uri)

    db = client['stock_predict']
    buy_signal_collection = db['buy_signal_track']
    training_data_collection = db['training_data']
    lstm_training_data_collection = db[env.COLLECTION_LSTM_TRAINING_DATA]
    collection_lstm_prediction = db['lstm_prediction']

    # Calculate the cut off date for the cleaning
    cut_off_date = datetime.now() - timedelta(days=env.cleaner_days_old)
    # cut_off_date = datetime.now()

    # Delete old tracked data from the buy_signal_track collection
    delete_result = buy_signal_collection.delete_many({"first_buy_signal_data": {"$lt": cut_off_date}})
    logger.info(f"{env.cleaner_module_name}: Cleaned old tracked stocks from DB:" +  str(delete_result.deleted_count))

    # Delete old model files
    training_old_data = training_data_collection.find({"training_date": {"$lt": cut_off_date}})
    list_old_training_data = list(training_old_data)
    list_old_training_data = [old_trainning.get('stock_title') for old_trainning in list_old_training_data]
    delete_model_files(list_old_training_data)

    # Delete lstm predictions 
    collection_lstm_prediction.delete_many({'stock_title': {'$in': list_old_training_data}})

    # Delete old training data from the training_data collection
    deleted_items_from_training_collection = training_data_collection.delete_many({"training_date": {"$lt": cut_off_date}})
    logger.info(f"{env.cleaner_module_name}:Cleaned old training data from DB trining collection:" +  str(deleted_items_from_training_collection.deleted_count))

    # delete old lstm training data 
    deleted_lstm_items_from_training_collection = lstm_training_data_collection.delete_many({"training_date": {"$lt": cut_off_date}})
    logger.info(f"{env.cleaner_module_name}:Cleaned old LSTM training data from DB trining collection:" +  str(deleted_lstm_items_from_training_collection.deleted_count))
    logger.info(f"{env.cleaner_module_name}:Old tracking data clean completed")

    logger.info(f"{env.cleaner_module_name}:Start prediction porocessing")
    return {"status":delete_result.deleted_count}

