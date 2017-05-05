import  pymongo
class handleMongo():
    @classmethod
    def get_mongo(cls):
        client=pymongo.MongoClient(host='localhost',port=27017)
        return client
