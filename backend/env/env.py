# flask routes
# base route 
base_url = 'http://127.0.0.1:5000'
#  store data to mongo
route_store_data_mongo = '/trend-calculation-store-to-db'
#  indicator calculation
route_indicator_calculation = '/indicators_generation'
#  collect buy signal
route_collect_buy_signal = '/collect-buy-signal-stock'
# nn_training_model 
route_nn_training_model = '/nn-training-model'
# lstm training 
route_lstm_training_model = '/lstm-training-model'
# cleaner module
route_cleaner_module = '/cleaner-module'
# price predictor route 
route_price_predictor = '/predict-price'
# data pull route
route_stock_data_pull = '/stock-data-pull'
# model prepare route
route_model_train = '/model-train'
# model prediction route
route_prediction_module = '/prediction'
# start stocks prediction route 
route_start_prediction = '/prediction'
# start lstm prediction 
route_start_lstm_prediction = '/lstm-prediction'
# tracked stock metrics calculation route
route_tracked_stocks_metrics = '/tracked-stocks-metrics'
# news anylysis route
route_news_analysis = '/news-analysis'
# route web api main route 
route_web_api_main = "/"
# route web api /stock-data/
route_web_api_stock_data = "/stock-data/"
# route web api /tracked-stocks/ 
route_web_api_tracked_stocks = "/tracked-stocks/"
# route buy signal all stock 
route_web_api_buy_signal_all_stocks = "/buy-signal-all-stocks"
# route web api "/training-data/ 
route_web_api_training_data = "/training-data/"
# route web apii /result-data/
route_web_api_result_data = "/result-data/"
# route web api /stock-sentiment/
route_web_api_stock_sentiment = "/stock-sentiment/"
# routre lstm prediction /lstm-predictions/ 
route_web_api_lstm_prediction = "/lstm-predictions/"
# packages NAMES 
# first_stock_data_fetch
first_data_fetch_module_name = 'FIRST_DATA_FETCH_MODULE'
# stock_indicator_calculation
stock_indicator_calculation_module_name = 'STOCK_INDICATOR_CALCULATION_MODULE'
# store_data_to_monog
store_data_mongo_name = 'STORE_DATA_TO_MONGO_MODULE'
# collect_buy_signal_stock
collect_buy_signal_name = 'COLLECT_BUY_SIGNAL_MODULE'
# cleaner module 
cleaner_module_name = 'CLEANER_MODULE'
# lst prediction module name 
lstm_module_prediction_name = 'LSTM_PREDICTION_NAME'
# stock names
STOCK_CSV_DATA_FAIL = "constituents.csv"
# Mongo database setup
# db url
URL_MONGO = "mongodb://localhost:27017/"
# db name
DB_NAME = "stock_predict"
# collection names
COLLECTION_NAME_STOCKS_UNDER_TRACKING = "buy_signal_track"
# SP 500 stock data pull days
COLLECTION_NAME_SP500_STOCKS_DATA = "sp500_stocks_data"
# colection training data 
COLLECTION_NAME_TRAINING_DATA = "training_data"
# collection lstm training data 
COLLECTION_LSTM_TRAINING_DATA = "lstm_training_data"
# Mongo DB port number 
MONGO_DB_PORT_NUMBER = 27017
# stock filled name 
STOCK_TITLE_FILED_NAME = "stock_title"
# 14 days tracking filled 
TRACKING_FIELD_NAME_14_DAYS = "days_tracking"
# path for NN models store 
model_path: str = f"model_trainning/nn_model/models/"
# path for LSTM model 
lstm_model_path: str = f"model_trainning/lstm_model/models/"
# days pull for stock data
stock_data_pull_days = 365
# stock cleaner days old 
cleaner_days_old = 14
# RSI treshold 
RSI_THRESHOLD = 30
# BUY SIGAL COEFFICIENT
BUY_SIGNAL_COEFFICIENT = 1
# Moving average window size 
MOVING_AVERAGE_WINDOW_SIZE = 14
# RSI window size
RSI_WINDOW_SIZE = 14
# Column for calculations  - close 
COLUMN_CALCULATION_NAME_RSI = 'Close'
# Stock title
STOCK_TITLE_FILED_NAME = 'stock_title'
# NUMBER OF STOCKS TO RUN 
NUMBER_OF_STOCKS_TO_RUN = 490
# FININ KEY 
FIN_KEY = "d0nm841r01qn5ghkk9g0d0nm841r01qn5ghkk9gg"
# lstm sequince lenght 
lstm_sequence_length = 60  # e.g., use past 60 days to predict next 5
# lstm days predict
lstm_future_days = 5
# backend apis
blue_print_back_end_api = "blue_print_web_api"
