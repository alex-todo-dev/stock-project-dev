# That module will pick up close price and predict the future price for the next day 
from flask import Flask, request, Blueprint
from env import env
from logger import logger
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import json
import numpy as np 
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

prediction_module_lstm = Blueprint(env.route_start_lstm_prediction, __name__)
# Pull all tracked stock from buy_signal_track collection

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client['stock_predict']
collection_stock_data = db['sp500_stocks_data']
collection_stocks_under_tracking = db['buy_signal_track']
collection_lstm_prediction = db['lstm_prediction']

@prediction_module_lstm.route(env.route_start_lstm_prediction, methods=['GET'])
def predict_price():
    from .next_five_working_days import next_five_working_days
    logger.info(f"{env.lstm_module_prediction_name} : ****************************")
    logger.info(f"{env.lstm_module_prediction_name} : Starting lstm prediction")
    print("Staring lsmt prediction")

    tracked_stocks = collection_stocks_under_tracking.find()
    tracked_stocks_list = list(tracked_stocks)

    for tracked_stock in tracked_stocks_list:
        tracked_stock_title = tracked_stock.get('stock_title')
        logger.info(f"{env.lstm_module_prediction_name} : Prediction next five days for {tracked_stock_title}")
        first_buy_signal_date = tracked_stock.get('first_buy_signal_data')
        tracking_data_14_days = tracked_stock.get('days_tracking')

        # Check if lstm if already predicted for next five work days 
        

        # Loadind model and scaler 
        from tensorflow.keras.models import load_model
        import joblib
        try:
            model = load_model(env.lstm_model_path  + tracked_stock_title + '_lstm.h5' , compile=False)
            scaler = joblib.load(env.lstm_model_path + tracked_stock_title + '_lstm_scaler.save')
            scaler_rsi = joblib.load(env.lstm_model_path + tracked_stock_title + '_lstm_rsi_scaler.save')
        except:
            logger.error(f"{env.lstm_module_prediction_name} : Failed to load model for stock {tracked_stock_title}")
            print('Failed to load the model')

        print(f'Loaded data for lstm model {tracked_stock_title}')
        logger.info(f"{env.lstm_module_prediction_name} : Loaded model for {tracked_stock_title}")

        # Loading stock for current date and predicting next day close price
        stock_data = collection_stock_data.find_one({"stock_title": tracked_stock_title}) 

        # Loading data table with last year data 
        stock_table_data = stock_data['data_frame']
        stock_data_df = pd.DataFrame(json.loads(stock_table_data))
        

        # extract last 60 rows
        # Sort and select last 60 rows
        df_latest = stock_data_df.sort_values('Date').dropna(subset=['Close', 'RSI']).copy()
        df_input = df_latest.tail(60)

        # print(stock_data_df_sorted)
        # Transfer to 3d array 
        # print(stock_data_df_sorted)
        
        
        # Last dey from pulled data 
        last_date = df_input.iloc[-1]['Date']
        last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")

        # If there are predictions for that stock 
        existing_prediciton_doc =  collection_lstm_prediction.find_one({"stock_title":tracked_stock_title},{"_id": 0})
        if existing_prediciton_doc: 
            print(f"Found lstm prediction for {tracked_stock_title}")
            results_list = existing_prediciton_doc.get('next_five_day_predictions')
            last_predicted_date_obj = results_list[-1]
            last_predicted_date = last_predicted_date_obj.get('date')
            print("last day:",last_predicted_date)

            # check if last date in db is less than predicited 
            if last_date_obj <= last_predicted_date:
                logger.info(f"{env.lstm_module_prediction_name} : Stock {tracked_stock_title} lstm prediction exists and will be canceled")
                print("Data base date is less and cancel prediction")
                continue
            else:
                # delete prediction because prediction is already in mongo 
                logger.info(f"{env.lstm_module_prediction_name} : Stock {tracked_stock_title} will predict")
                print("Not found data in predictions, will do predict")
                # collection_lstm_prediction.delete_many({"stock_title":tracked_stock_title})
                

        # print(f'Last date:{last_date}')
        next_five_days = next_five_working_days(last_date)
        # print(f'Next five days:{next_five_days}')
       
        # Scale features
        close_scaled = scaler.transform(df_input[['Close']])
        rsi_scaled = scaler_rsi.transform(df_input[['RSI']])
        
        # Combine into LSTM input
        X_input = np.column_stack((close_scaled, rsi_scaled))  # shape (60, 2)
        X_input = np.expand_dims(X_input, axis=0)     

        pred_scaled = model.predict(X_input)  # shape: (1, 5)
        pred_scaled = pred_scaled.flatten()

        predicted_prices = scaler.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()

        # Createing list of objects 
        # Convert strings to date objects and zip with prices
        result = []

        # grouping next five days dates and prediction results
        for date_str, price in zip(next_five_days, predicted_prices):
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            # Convert date to datetime for MongoDB compatibility
            datetime_obj = datetime.combine(date_obj, datetime.min.time())
            result.append({'date': datetime_obj, 'price': float(price)})

        # insert results in mongo
        results_insert = {
            "stock_title" : tracked_stock_title,
            "next_five_day_predictions": result 
        }
        print("Insert data")

        print(results_insert)
        # Append each prediction to the matching document
        

        # collection_lstm_prediction.insert_one(results_insert)
        existing_doc = collection_lstm_prediction.find_one({"stock_title":tracked_stock_title},{"_id": 0})
        
        # check if alredy exist doc for that stock and append the data 
        if existing_doc:
            collection_lstm_prediction.update_one(
                {"stock_title": tracked_stock_title},
                {"$push": {"next_five_day_predictions": {"$each": result}}},
                upsert=True
            );
        # firts time append
        else:
            collection_lstm_prediction.insert_one(results_insert)
    return {"status":"lstm prediction finished"}