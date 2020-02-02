import pymongo
from pymongo import MongoClient

ENV = "test"

if ENV.lower() == "production":

    MONGO_DB_NAME = 'image_search'
    MONGO_DB_URL = 'localhost'
 
else:

    MONGO_DB_NAME = 'image_search_local'
    MONGO_DB_URL = 'localhost'
 
CLIENT = MongoClient()
CLIENT = MongoClient(MONGO_DB_URL, 27017)
DB = CLIENT[MONGO_DB_NAME]
