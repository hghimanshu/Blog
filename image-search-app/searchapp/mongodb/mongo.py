import pymongo
from pymongo import MongoClient
import sys
from searchapp.config.settings import MONGO_DB_NAME, MONGO_DB_URL, DB


class settingupDb:
    def __init__(self, query, coll_name):
        self.query = query
        self.coll_name = coll_name
    def construct_Db(self):
        self.coll = DB[self.coll_name]
        return self.coll





def push_into_db(self,db,coll,query):
    self.post_id = coll.insert(self.query, check_keys=False)
    print('Data inserted for Object ID:: ',self.post_id)
def updates_info(self, db, coll, query, newVal):
    self.query = query
    self.newVal = newVal
    self.updatedColl = coll.update_many(self.query, self.newVal)
    print(self.updatedColl.modified_count,'Documents updated !!')
