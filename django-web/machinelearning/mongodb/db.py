# -*- coding:utf-8 -*-
import  pymongo
class Mongo():
    @classmethod
    def get_mongo(cls):
        client=pymongo.MongoClient(host='localhost',port=27017)
        return client
