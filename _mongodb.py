from bson.objectid import ObjectId
class MongoDBPython():
    def __init__(self,db) -> None:
        self.collection = db['notification']

    def insert_data(self,data):
        inserted_id = self.collection.insert_one(data).inserted_id
        return inserted_id

    def update_data(self,id,data):
        self.collection.update_one({"_id": ObjectId(id)}, {"$set":{"status":data}})

    def get_all_twitter_key_phrases(self):
        twitter_keyphrase_list = list()
        for i in self.collection.find({},{"key_phrase":1,"start_date":1,"end_date":1}):
            i['_id'] = str(i['_id'])
            twitter_keyphrase_list.append(i)

        return twitter_keyphrase_list
        
    def get_specific_keyphrasedata(self,keyphrase_id):
        return self.collection.find_one({"_id":ObjectId(keyphrase_id)},{"_id":0,"data":1})