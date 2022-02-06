from bson.objectid import ObjectId
class MongoDBPython():
    def __init__(self,db) -> None:
        self.collection = db['twitter_collection']

    def insert_data(self,data):
        inserted_id = self.collection.insert_one(data).inserted_id
        return inserted_id

    def update_data(self,id,data):
        self.collection.update_one({"_id": ObjectId(id)}, {"$set":{"data":data}})
        