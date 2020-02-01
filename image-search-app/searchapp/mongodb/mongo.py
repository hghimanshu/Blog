import pymongo
from pymongo import MongoClient
import sys
from searchapp.config.settings import DB


class settingupDb:
    def __init__(self, query, coll_name):
        self.query = query
        self.coll_name = coll_name

    def constructDb(self):
        self.coll = DB[self.coll_name]
        return self.coll

    def insertsToDb(self,db,coll,query):
        self.post_id = coll.insert(self.query, check_keys=False)
        print('Data inserted for Object ID:: ',self.post_id)

    def updatesInfo(self, db, coll, query, newVal):
        self.query = query
        self.newVal = newVal
        self.updatedColl = coll.update_many(self.query, self.newVal)
        print(self.updatedColl.modified_count,'Documents updated !!')

    def fetchInfo(self, db, coll, query):
        self.results = coll.find(query)
        return self.results

    def deleteInfo(self, db, coll, query):
        self.results = coll.delete_many(query)
        print(self.results.deleted_count, " documents deleted.") 
        return self.results
