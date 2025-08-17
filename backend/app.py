from flask import Flask
from store_data_to_mongo.store_db_api import store_stock_data_to_mongo_module
from stock_indicator_calculation.indicators_calculation_web_api import indicator_calculation_module
from collect_buy_signal_stock.collect_buy_signal_stocks_api import collection_buy_signal_store_module
from model_trainning.nn_model.model_train_api import nn_model_train_module
from cleaner.old_tracking_clean import clean_module
from first_stock_data_fetch.data_pull import data_pull_module
from model_trainning.data_processor import model_generation_module
from prediction_module.predicition_module_api import prediction_module
from tracked_stocks_metrics.tracked_stock_metrics_calc_api import tracked_stocks_metrics_module
from stock_news.stock_news_api import news_analysis_module
from model_trainning.lstm_model.lstm_train_api import lstm_model_train_module
from prediction_module_lstm.predict_next_five_days_api import prediction_module_lstm
from back_end_web_api.web_api import web_api_module
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(model_generation_module)
app.register_blueprint(data_pull_module)
app.register_blueprint(indicator_calculation_module)
app.register_blueprint(store_stock_data_to_mongo_module)
app.register_blueprint(collection_buy_signal_store_module)
app.register_blueprint(nn_model_train_module)
app.register_blueprint(clean_module)
app.register_blueprint(prediction_module)
app.register_blueprint(tracked_stocks_metrics_module)
app.register_blueprint(news_analysis_module)
app.register_blueprint(lstm_model_train_module)
app.register_blueprint(prediction_module_lstm)
app.register_blueprint(web_api_module)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    # docker run --name mongodb -d -p 27017:27017 -v mongodata:/data/db mongo
