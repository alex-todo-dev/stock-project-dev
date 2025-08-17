from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from flask import Blueprint
from env import env
import os 


web_api_module = Blueprint(env.blue_print_back_end_api, __name__)

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)


db = client["stock_predict"]  # your database name
tracked_stocks_collection = db["buy_signal_track"]  # your collection name
trade_stock_data_collection = db["sp500_stocks_data"]
training_data_collection = db["training_data"]
prediction_metrics_collection = db["tracked_stock_metrics"]
news_sentiment_collection = db["stock_news_sentimental"]
lstm_predictions_collection = db["lstm_prediction"]

@web_api_module.route(env.route_web_api_main, methods=["GET"])
def home():
    return "Welcome to the Stock Predictor Home Page api!"

@web_api_module.route(env.route_web_api_stock_data + "<stock>", methods=["GET"])
def stock_data(stock: str) -> dict:
    stock_data = trade_stock_data_collection.find_one({"stock_title": stock},{'_id': 0})
    return jsonify(stock_data) 

@web_api_module.route(env.route_web_api_tracked_stocks + "<stock>")
def tracked_stocks(stock: str):
    tracked_stocks = tracked_stocks_collection.find({"stock_title": stock},{'_id': 0})
    return jsonify(tracked_stocks)

@web_api_module.route(env.route_web_api_buy_signal_all_stocks)
def all_tracked_stocks():
    all_tracked_stocks = tracked_stocks_collection.find({},{'_id': 0})
    return jsonify(list(all_tracked_stocks))

@web_api_module.route(env.route_web_api_training_data + "<stock>")
def training_data(stock: str):
    stock_training_data = training_data_collection.find_one({"stock_title": stock},{'_id': 0})
    return jsonify(stock_training_data)

@web_api_module.route(env.route_web_api_result_data + "<stock>")
def result_data(stock: str):
    prediction_result_data = prediction_metrics_collection.find_one({"stock_title": stock},{'_id': 0})
    return jsonify(prediction_result_data)

@web_api_module.route(env.route_web_api_stock_sentiment +  "<symbol>", methods=['GET'])
def get_stock_sentiment(symbol):
    doc = news_sentiment_collection.find_one({"stock_title": symbol})

    if doc:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string for JSON serialization
        return jsonify(doc)
    else:
        return jsonify(None)

@web_api_module.route(env.route_web_api_lstm_prediction + "<stock>", methods=['GET'])
def get_stock_lstm_prediction(stock: str):
    lstm_doc = lstm_predictions_collection.find_one({"stock_title": stock},{'_id': 0})
    return jsonify(lstm_doc)



# if __name__ == "__main__":
#     app.run(port=5001, debug=True)
