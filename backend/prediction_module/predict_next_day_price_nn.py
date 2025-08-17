from env import env
from logger import logger
from tensorflow.keras.models import load_model
import pickle
from pymongo import MongoClient
import keras
from keras.losses import MeanSquaredError
import pandas as pd 
import json 
import joblib
import os 

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client

client = MongoClient(mongo_uri)
db = client['stock_predict']
collection_data = db['sp500_stocks_data']
collection_stocks_under_tracking = db['buy_signal_track']


def predict_next_day_price(stock_title,current_day):
    print(f"Calculating the next day price with NN model for {stock_title}")
    print(f"Current day__: {current_day}")
    next_day_close_price_prediction = None 

    # Load the model and scaler
    try:
        mse = MeanSquaredError()
        model = keras.models.load_model(env.model_path + f"{stock_title}.h5", custom_objects={"mse": mse})
        # Load the scaler from the pickle file
        # with open(env.model_path + f"{stock_title}.pkl", 'rb') as file:
        #     loaded_scaler = pickle.load(file)

        # Load the scaler from the file
        loaded_scaler = joblib.load(env.model_path + f"{stock_title}.pkl")
    except Exception as e:
        logger.error(f"Failed to load model and scaler for {stock_title}: {e}")
        print(f"Failed to load model and scaler for {stock_title}: {e}")
        return None
    print("Model loaded successfully")

    # comile the loaded model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    print("Loaded model compiled successfully")
    # Loading stock for current date and predicting next day close price
    stock_data = collection_data.find_one({"stock_title": stock_title}) 
   
    # Loading data table with last year data 
    stock_table_data = stock_data['data_frame']
    stock_data_df = pd.DataFrame(json.loads(stock_table_data))

    # Loadind data data for the current day 
    stock_data_df['Date'] = pd.to_datetime(stock_data_df['Date'])
    filtered_row = stock_data_df[ stock_data_df['Date'].dt.date== current_day]
    print("Stock data loaded successfully")

    # Generating day an month column 
    filtered_row['day'] = filtered_row['Date'].dt.day
    filtered_row['month'] = filtered_row['Date'].dt.month
    
    # Predicting next day close price
    # next_day_close_price_prediction = model.predict(loaded_scaler.transform(filtered_row.drop(columns=['Date'])))
    filtered_row.drop(columns=['Date'], inplace=True)

    # transforming the data
    new_data_scaled = loaded_scaler.transform(filtered_row.values)
    # new data prediction 
    next_day_close_price_prediction = model.predict(new_data_scaled)
    return next_day_close_price_prediction