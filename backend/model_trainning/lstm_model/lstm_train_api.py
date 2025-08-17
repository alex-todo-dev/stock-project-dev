# That train and save the model for tracked stock
from env import env
from pymongo import MongoClient
import pandas as pd
from flask import Blueprint, request
import json
import os 
from logger import logger
from datetime import datetime
import numpy as np

lstm_model_train_module = Blueprint(env.route_lstm_training_model, __name__)

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client[env.DB_NAME]
collection_stocks_data = db[env.COLLECTION_NAME_SP500_STOCKS_DATA]
collection_lstm_training_data = db[env.COLLECTION_LSTM_TRAINING_DATA]

@lstm_model_train_module.route(env.route_lstm_training_model,methods=['POST'])
def train_lstm_model() -> dict:
    data: dict = request.get_json()
    print("LSTM Trainer:", data)
    stock_title: str = data['stock_title']

    lstm_model_path: str = env.lstm_model_path + f"{stock_title}_lstm.h5"
    lstm_scaler_path:str = env.lstm_model_path + f"{stock_title}_lstm_scaler.save"
    lstm_scler_rsi_path:str = env.lstm_model_path + f"{stock_title}_lstm_rsi_scaler.save"

    # check if model if already exits and saved 
    if os.path.exists(lstm_model_path) and os.path.exists(lstm_scaler_path):
        logger.info(f"LSTM MODEL TRAINNER:LSTM model already exist for {stock_title}, will skip training")
        print("Model already exists")
        return {"status": " lstml model already exists"}, 200

    # start training new model
    logger.info(f"LSTM MODEL TRAINNER:LSTM model not found {stock_title}, starting training")
    stock_data: dict = collection_stocks_data.find_one({"stock_title": stock_title})
    if not stock_data:
        return {"status": "stock not found"}, 404
    df_str: str = stock_data['data_frame']
    if not df_str:
        return {"status": "no data for stock"}, 400
    df: pd.DataFrame = pd.DataFrame(json.loads(df_str))

    # data preparation 
    from sklearn.preprocessing import MinMaxScaler

    # Sort by date
    df = df.sort_values('Date')

    # Drop NA 
    df = df.dropna(subset=['RSI', 'Close']) 

    # Scale only the 'Close' column for prediction
    scaler = MinMaxScaler()

    # Scale both Close and RSI
    scaler_close = MinMaxScaler()
    scaler_rsi = MinMaxScaler()

    # features scale
    df['Close_scaled'] = scaler_close.fit_transform(df[['Close']])
    df['RSI_scaled'] = scaler_rsi.fit_transform(df[['RSI']])
     
    sequence_length = env.lstm_sequence_length  # e.g., use past 60 days to predict next 5
    future_days = env.lstm_future_days
    
    # Build sequences
    X, y = [], []
    close = df['Close_scaled'].values
    rsi = df['RSI_scaled'].values

    for i in range(len(df) - sequence_length - future_days + 1):
        seq = np.column_stack((close[i:i+sequence_length], rsi[i:i+sequence_length]))  # shape (60, 2)
        X.append(seq)
        y.append(close[i+sequence_length:i+sequence_length+future_days])  # shape (5,)

    X, y = np.array(X), np.array(y)

    
    # Models create
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
    from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
    import joblib

    # ---------------- MODEL ---------------- #
    model = Sequential([
        LSTM(64, return_sequences=False, input_shape=(X.shape[1], X.shape[2])),  # (60, 2)
        Dense(future_days)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.summary()

    # ---------------- CALLBACKS ---------------- #
    checkpoint = ModelCheckpoint(
        lstm_model_path,
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )

    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )


    # ---------------- TRAIN ---------------- #
    history = model.fit(
        X, y,
        epochs=1000,
        batch_size=32,
        validation_split=0.1,
        callbacks=[checkpoint, early_stop],
        verbose=1
    )

    # ---------------- SAVE SCALERS ---------------- #
    joblib.dump(scaler_close, lstm_scaler_path)
    joblib.dump(scaler_rsi, lstm_scler_rsi_path)

 
    
    # ---------------- METRICS TO MONGO ---------------- #
    final_train_mse = float(history.history['loss'][-1])
    final_val_mse = float(history.history['val_loss'][-1])


    metrics_doc = {
    "model_name": "lstm_close_rsi",
    "date_trained": datetime.now(),
    "train_mse_scaled": final_train_mse,
    "val_mse_scaled": final_val_mse,
    "sequence_length": sequence_length,
    "future_days": future_days}

    collection_lstm_training_data.insert_one(metrics_doc)

        
    logger.info(f"MODEL TRAINNER:Model trained for {stock_title} finished and saved, with MAR: {final_val_mse}")


    return {"status":"succes"}
