# That module will pick up close price and predict the future price for the next day 
from flask import Flask, request, Blueprint
from env import env
from logger import logger
from pymongo import MongoClient
from datetime import datetime
import os 


# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client['stock_predict']

collection = db['buy_signal_track']


collection_stock_data = db['sp500_stocks_data']
collection_stocks_under_tracking = db['buy_signal_track']

prediction_module = Blueprint(env.route_prediction_module, __name__)
# Pull all tracked stock from buy_signal_track collection



@prediction_module.route(env.route_prediction_module, methods=['GET'])
def predict_price():
    from .next_working_day import next_working_day
    from .predict_next_day_price_nn import predict_next_day_price
    logger.info("********************************************************")
    logger.info(f"{env.route_prediction_module}: Prediction module started")

    tracked_stocks = collection_stocks_under_tracking.find()
    tracked_stocks_list = list(tracked_stocks)
    for tracked_stock in tracked_stocks_list:
        # print("Stock:", tracked_stock)
        tracked_stock_title = tracked_stock.get('stock_title')
        first_buy_signal_date = tracked_stock.get('first_buy_signal_data')
        tracking_data_14_days = tracked_stock.get('days_tracking')
        # print("Stock_data:", tracking_data_14_days)
        # filtering items that were no predicted yet 
        tracking_data_14_days = [date_item for date_item in tracking_data_14_days if date_item['predicted_price'] == False]
        # print("Data_dates:",tracking_data_14_days)
        for day_data in tracking_data_14_days:
            # need to skip dates that already has predicstions in mongo
            tracked_stock_date = day_data['date'].date()
            current_day_closing_price = day_data['closing_price']
         
            # next_work_day
            next_work_day = next_working_day(tracked_stock_date)
         
            # prediction for the next day day 
            next_day_price_prediction = predict_next_day_price(tracked_stock_title, tracked_stock_date)
            print(f"Stock {tracked_stock_title}, current day: {tracked_stock_date}, curent price: {current_day_closing_price}")
            print(f"Stock {tracked_stock_title}, date:{next_work_day} next day price prediction:{next_day_price_prediction}")

            next_work_day_datetime = datetime.combine(next_work_day, datetime.min.time())
            current_stock_day_datetime = datetime.combine(tracked_stock_date, datetime.min.time())

            new_predicted_value = {"date": next_work_day_datetime, "closing_price": float(next_day_price_prediction[0][0])}
            print("Value to import:", new_predicted_value)

            # Updateting results in MongoDB 
            query = {"stock_title": tracked_stock_title}
            update_result_new_predicted = collection.update_one(query, {"$push": {"next_day_predictions": new_predicted_value}})

            query_udpate_predcited = {"stock_title": tracked_stock_title, "days_tracking.date": current_stock_day_datetime}
            udapte_predicted_price = collection.update_one(query_udpate_predcited,{"$set": {"days_tracking.$.predicted_price": True}})

    return {"status": "success"}, 200