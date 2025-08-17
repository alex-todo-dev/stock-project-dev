import json
from flask import request, Blueprint
from logger import logger
import pandas as pd
from env import env
import requests
from datetime import datetime
from typing import Dict, Any

# Create a new Blueprint for the indicator calculation module
indicator_calculation_module = Blueprint(env.route_indicator_calculation, __name__)

@indicator_calculation_module.route(env.route_indicator_calculation, methods=['POST'])
def indicator_calculation() -> Dict[str, str]:
    """
    Endpoint to perform indicator calculations for a given stock.
    
    The function retrieves stock data from the request, performs RSI,
    moving average, and buy signal calculations, and sends the results
    to a MongoDB storage service.
    
    Returns:
        A dictionary with a single key 'status' and a value of 'data arrived'
    """
    from .calculate_rsi import calculate_rsi
    from .calculate_moving_average import calculate_moving_average
    from .buy_signal_calculation import generate_buy_signal
    
    logger.info(f"{env.stock_indicator_calculation_module_name}: Stock data received to indicators calculation")
    
    # Parse JSON data from the request
    data: Dict[str, Any] = request.get_json()
    stock_title: str = data.get('title')
    stock_data: str = data.get('table')
    beta: float = data.get('beta')
    
    if not stock_title or not stock_data or not beta:
        logger.error(f"{env.stock_indicator_calculation_module_name}: Missing required data for stock {stock_title}")
        return {"status": "missing data"}
    
    logger.info(f"{env.stock_indicator_calculation_module_name}: Stock data received to indicators calculation for stock {stock_title}")
    
    # Create a DataFrame from the stock data
    try:
        stock_df: pd.DataFrame = pd.DataFrame(json.loads(stock_data))
    except json.JSONDecodeError:
        logger.error(f"{env.stock_indicator_calculation_module_name}: Error parsing JSON data for stock {stock_title}")
        return {"status": "invalid data"}
    
    #  RSI calculation
    try:
        stock_df: pd.DataFrame = calculate_rsi(stock_df)
    except Exception as e:
        logger.error(f"{env.stock_indicator_calculation_module_name}: Error performing RSI calculation for stock {stock_title}: {e}")
        return {"status": "error"}
    logger.info(f"{env.stock_indicator_calculation_module_name}: {stock_title} - RSI calculation done")
    
    # Moving average calculation
    try:
        stock_df: pd.DataFrame = calculate_moving_average(stock_df)
    except Exception as e:
        logger.error(f"{env.stock_indicator_calculation_module_name}: Error performing moving average calculation for stock {stock_title}: {e}")
        return {"status": "error"}
    logger.info(f"{env.stock_indicator_calculation_module_name}: {stock_title} - Moving average calculation done")
    
    # Buy signal calculation
    try:
        stock_df: pd.DataFrame = generate_buy_signal(stock_df)
        stock_df.to_csv('testing_data.csv')
    except Exception as e:
        logger.error(f"{env.stock_indicator_calculation_module_name}: Error performing buy signal calculation for stock {stock_title}: {e}")
        return {"status": "error"}
    logger.info(f"{env.stock_indicator_calculation_module_name}: {stock_title} - Buy indicator calculation done")
    
    # Extract the last day's data for storage
    last_day_data_dict: Dict[str, Any] = stock_df.iloc[-1].to_dict()
    json_stock_data_json: str = stock_df.to_json(orient='records')
    
    # Prepare JSON data for storage in MongoDB
    json_for_store_in_db: Dict[str, Any] = {
        "stock_title": stock_title,
        "last_day_date": last_day_data_dict['Date'],
        "beta": beta,
        "last_closing_price": last_day_data_dict['Close'],
        "last_buy_signal": {"signal": last_day_data_dict['Buy_signal'], "date": last_day_data_dict['Date']},
        "data_frame": json_stock_data_json
    }
    
    # Send the processed data to the storage service
    try:
        response_from_trend_calc: requests.Response = requests.post(env.base_url + env.route_store_data_mongo, json=json_for_store_in_db)
    except requests.exceptions.RequestException as e:
        logger.error(f"{env.stock_indicator_calculation_module_name}: Error sending data to Store_to_mongo module for stock {stock_title}: {e}")
        return {"status": "error"}
    logger.info(f"{env.stock_indicator_calculation_module_name}: {stock_title} - data sent to Store_to_mongo module")
    
    # Return a success status
    return {"status": f"Stock {stock_title} indicator caluclation completed"}

