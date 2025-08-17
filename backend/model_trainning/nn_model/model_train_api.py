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

nn_model_train_module = Blueprint(env.route_nn_training_model, __name__)

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client[env.DB_NAME]
collection_stocks_data = db[env.COLLECTION_NAME_SP500_STOCKS_DATA]
collection_training_data = db[env.COLLECTION_NAME_TRAINING_DATA]

@nn_model_train_module.route(env.route_nn_training_model,methods=['POST'])
def train_model() -> dict:
    """
    Train and save a neural network model for the specified stock.

    Expects a JSON payload with 'stock_title' and 'tracking_data_14_days'.

    :return: A dictionary with the status of the operation.
    :rtype: dict
    """
    data: dict = request.get_json()
    print("Trainer:", data)
    stock_title: str = data['stock_title']
    # tracking_data_14_days: list = data['tracking_data_14_days']

    # Check if model and scaler already exist
    model_path: str = env.model_path + f"{stock_title}.h5"
    scaler_path: str = env.model_path + f"{stock_title}.pkl"
    logger.info(f"MODEL TRAINNER:Checking if model and scaler already exist for {stock_title}")
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        logger.info(f"MODEL TRAINNER:Model and scaler already exist for {stock_title}, will skip training")
        return {"status": "model already exists"}, 200
    logger.info(f"MODEL TRAINNER:Model and scaler not found for {stock_title}, starting training")
    stock_data: dict = collection_stocks_data.find_one({"stock_title": stock_title})
    if not stock_data:
        return {"status": "stock not found"}, 404

    df_str: str = stock_data['data_frame']
    if not df_str:
        return {"status": "no data for stock"}, 400

    df: pd.DataFrame = pd.DataFrame(json.loads(df_str))
    df['target'] = df['Close'].shift(-1)
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['day'] = df['Date'].dt.day
    df['month'] = df['Date'].dt.month

    feature_columns: list = [col for col in df.columns if col not in ['target', 'Date']]
    X: pd.DataFrame = df[feature_columns]
    y: pd.Series = df['target']

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=10)
    from sklearn.preprocessing import StandardScaler
    import joblib
   
    scaler: StandardScaler = StandardScaler()
    X_train_scaled: pd.DataFrame = scaler.fit_transform(X_train)
    X_test_scaled: pd.DataFrame = scaler.transform(X_test)
   
    joblib.dump(scaler, env.model_path + f"{stock_title}.pkl")
    # joblib.dump(X_test_scaled, env.model_path + f"{stock_title}.pkl")
    # with open(env.model_path + f"{stock_title}.pkl", 'wb') as file:
    #     pickle.dump(X_test_scaled, file)
        
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.callbacks import EarlyStopping
    from sklearn.metrics import mean_absolute_error
    


    model = Sequential([
        Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        Dense(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=0, mode='min', restore_best_weights=True)

    model.fit(X_train_scaled, y_train, epochs=1000, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

    loss: float = model.evaluate(X_test_scaled, y_test)

    model.save(env.model_path + f"{stock_title}.h5")
    predictions: np.ndarray = model.predict(X_test_scaled)

    mse: float = mean_absolute_error(y_test, predictions)
    print(f"Mean Absolute Error: {mse}")
    # import matplotlib.pyplot as plt
    # import matplotlib
    # matplotlib.use('Agg')
    # plt.figure(figsize=(14, 7))
    # plt.plot(y_test.values, label='Actual')
    # plt.plot(predictions, label='Predicted')
    # plt.legend()
    # plt.savefig('predicted_vs_actual.png')
    df_result: pd.DataFrame = pd.DataFrame({
        'Actual': y_test.values.ravel(),
        'Predicted': predictions.ravel()
    })
    collection_training_data.insert_one({"training_date": datetime.now(),"stock_title": stock_title, "mse": mse})    
    logger.info(f"MODEL TRAINNER:Model trained for {stock_title} finished and saved, with MAR: {mse}")
    # df_result.to_csv('predicted_vs_actual.csv', index=False)
    return {"status": "model trained"}

