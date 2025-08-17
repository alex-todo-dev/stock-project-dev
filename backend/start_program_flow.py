import requests
from env import env
requests.get(env.base_url + env.route_stock_data_pull)
requests.post(env.base_url + env.route_cleaner_module)
requests.post(env.base_url + env.route_model_train)
requests.get(env.base_url + env.route_start_prediction)
requests.get(env.base_url + env.route_start_lstm_prediction)
requests.get(env.base_url + env.route_tracked_stocks_metrics)
requests.get(env.base_url + env.route_news_analysis)


# json_data = {
#             "stock_title": "MMM"
#         }
# response = requests.post(env.base_url + env.route_lstm_training_model, json = json_data)
# print(response)
