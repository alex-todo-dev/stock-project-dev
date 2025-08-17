import pandas as pd
import yfinance as yf
from datetime import timedelta, date
import requests
from env import env
from logger import logger
from flask import Blueprint
import time
data_pull_module = Blueprint(env.route_stock_data_pull, __name__)

@data_pull_module.route('/stock-data-pull')
def data_pull() -> str:
    """
    Fetches stock data for a list of stock symbols from a CSV file, processes the data, and sends it to an indicator calculation module.

    Returns:
        str: A message indicating completion of the data pull process.
    """

    stocks_data: pd.DataFrame = pd.read_csv('./first_stock_data_fetch/' + env.STOCK_CSV_DATA_FAIL)
    stock_names_list: list[str] = stocks_data['Symbol'].tolist()
    # Cleaning stock titles with . 
    stock_names_list = [stock for stock in stock_names_list if "." not in stock]

    days_delta: int = env.stock_data_pull_days

    for i, stock_name in enumerate(stock_names_list[:env.NUMBER_OF_STOCKS_TO_RUN]):
        logger.info("****************************************************************************")
        logger.info(f"{env.first_data_fetch_module_name}: pulling data for {stock_name}")
        
        try:
            # Download stock data for the last 365 days for stock  
            stock_data: pd.DataFrame = yf.download(stock_name, start=(date.today() - timedelta(days=days_delta)), end=date.today())
            # print("stock data:", stock_data)
            # Check if ffailed to downloaded data not correct 
            if not isinstance(stock_data, pd.DataFrame):
                logger.error(f"{env.first_data_fetch_module_name}: stock data for {stock_name} is not a dataframe")
                print("stock data for:", stock_name, "is not a dataframe")
                continue
            if stock_data.empty:
                logger.error(f"{env.first_data_fetch_module_name}:Yahoo api failed, failed to pull stock data for {stock_name}")
                print("failed to pull stock data for:", stock_name)
                continue
            
            # Fix column names 
            stock_data.columns = [col[0] for col in stock_data.columns]
            stock_data_index_reset: pd.DataFrame = stock_data.reset_index()
            stock_data_index_reset['Date'] = stock_data_index_reset['Date'].dt.strftime('%Y-%m-%d')

            # Convert stock data frame to json
            json_stock_data_json: str = stock_data_index_reset.to_json(orient='records')

            # pull stock beta
            stock_ticker = yf.Ticker(stock_name)
            beta: str = stock_ticker.info.get('beta', 'n/a')

            # Check if failed to pull beta
            if beta is None:
                logger.error(f"{env.first_data_fetch_module_name}: failed to pull beta for {stock_name}")
                print("failed to pull beta for:", stock_name)
                continue
            
            # Creating json object with stock data
            body_data: dict = {
                "id": i,
                "title": stock_name,
                "beta": beta,
                "table": json_stock_data_json,
            }

            logger.info(f"{env.first_data_fetch_module_name}: Stock data for {stock_name} pulled")
            response: requests.Response = requests.post(env.base_url + env.route_indicator_calculation, json=body_data)
            logger.info(f"{env.first_data_fetch_module_name}: {stock_name} stock json data sent for indicator calucation module")
            logger.info(f"{env.first_data_fetch_module_name}: {response} from {env.stock_indicator_calculation_module_name}")
            
        except Exception as e:
            logger.error(f"{env.first_data_fetch_module_name}: failed to pull stock data for {stock_name}")
            print("failed to pull stock data for:", stock_name, ':', e)
        time.sleep(1.5)  # delay to reduce 401s
    logger.info("****************************************************************************")
    logger.info(f"{env.first_data_fetch_module_name}: Data pull completed")
    logger.info("Starting data cleaner module")
    return "Data pull completed"


