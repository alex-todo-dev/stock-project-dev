from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def error_calculation(stock):
    stock_title = stock.get('stock_title')
    print(f"Calculating error for {stock_title} *****************************")
    days_tracking = stock.get('days_tracking')
    next_day_predictions = stock.get('next_day_predictions')
    error_result = {}
    predicted_closing_price_list = []
    real_closing_price_list = []

    for day_data in next_day_predictions:
        predicted_date = day_data.get('date')
        predicted_price = day_data.get('closing_price')
        result_real_price = next((d for d in days_tracking if d["date"] == predicted_date), None)
        if result_real_price:
            real_closing_price_list.append(result_real_price['closing_price'])
            predicted_closing_price_list.append(predicted_price)
        else:
            print(f"no real data found for {predicted_date}")
    # print("************************")
    # print("Real prices:", real_closing_price_list)
    # print("Predicted prices:", predicted_closing_price_list)
    if real_closing_price_list and predicted_closing_price_list:
        mae = mean_absolute_error(real_closing_price_list, predicted_closing_price_list)
        mse = mean_squared_error(real_closing_price_list, predicted_closing_price_list)
        rmse = np.sqrt(mse)
        error_result['MAE'] = mae
        error_result['MSE'] = mse
        error_result['RMSE'] = rmse
    return error_result
    