
from datetime import datetime
from logger import logger
from env import env
from pymongo import MongoClient
import os 

# Fetch Mongo URI from environment variable, fallback to localhost
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Create MongoDB client
client = MongoClient(mongo_uri)

db = client['stock_predict']
collection = db['sp500_stocks_data']

def store_data(stock_data):
    """
    Store the stock data to MongoDB
    
    Args:
    - stock_data (dict): the stock data to be stored
    
    Returns:
    - dict: {"stock": <stock title>, "status": <status>}
            - status: "replaced" if new data is newer than existing data 
            - status: "first time store" if it is the first time to store the stock
    """
    stock_title = stock_data[env.STOCK_TITLE_FILED_NAME]
    stock_data['store_time_stamp'] = datetime.now()
    stock_data_stored = collection.find_one({env.STOCK_TITLE_FILED_NAME: stock_title})

    # check if data for that stock is in DB 
    if stock_data_stored:
        logger.info(f"{env.store_data_mongo_name}: data already in DB for {stock_title}")
        # Extracts dates from strored stock date and just pull for compare  
        existing_stock_in_db_date = stock_data_stored.get('last_day_date')
        new_stock_date = datetime.strptime(stock_data.get('last_day_date'), "%Y-%m-%d") 

        # replace strind date with pyhton datetime 
        stock_data['last_day_date'] = new_stock_date

        # check if new date is older than existing
        if new_stock_date > existing_stock_in_db_date: 
            logger.info(f"{env.store_data_mongo_name}: replacing data for {stock_title}")

            # remove old data 
            delete_query = {env.STOCK_TITLE_FILED_NAME: stock_title}
            delete_result= collection.delete_many(delete_query)
            print("delete old data count:", delete_result)

            # inserts new data 
            insert_result =  collection.insert_one(stock_data)
            print("Insert resulst:", insert_result)
            return {"stock":stock_title, "status":"replaced"}
        # new stock has same date or before the stored one
        else: 
            print("New stock has same date or before the stored one:", stock_title)
            logger.info(f"{env.store_data_mongo_name}: New stock has same date or before the stored one - {stock_title}")
            return {"status":"done"}
        
    # first time store the stock 
    else:
        # replace strind date with pyhton datetime
        new_stock_date = datetime.strptime(stock_data.get('last_day_date'), "%Y-%m-%d")    
        stock_data['last_day_date'] = new_stock_date

        # New data insert 
        result =  collection.insert_one(stock_data)
        logger.info(f"{env.store_data_mongo_name}: First time store - {stock_title}")
        return {"stock":stock_title, "status":"first time store"}


