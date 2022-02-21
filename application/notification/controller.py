from datetime import timedelta
from datetime import datetime
from datetime import date
from bson.objectid import ObjectId

class NotificationController():
    def __init__(self,db) -> None:
        self.db = db
        self.collection = self.db['notification']

    def get_all_keyphrases(self):
        try:
            resp = {}
            twitter_keyphrase_list = list()
            for i in self.collection.find({},{"key_phrase":1,"start_date":1,"status":1} , sort=[( "_id", -1 )]):
                i['_id'] = str(i['_id'])
                twitter_keyphrase_list.append(i)
            resp['data'] = twitter_keyphrase_list
            return resp,200
        except Exception as e:
            return str(e),500

    def delete_keyphrase(self):
        for i in self.collection.find({},{"key_phrase":1,"start_date":1,"status":1}):
            date_value = datetime.strptime(i['start_date'],'%Y-%m-%d')
            if datetime.now() - date_value  > timedelta(days=5):
                self.collection.delete_one({"_id":ObjectId(i['_id'])})
        
        return "successfully removed"


def test_notification_controller():
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['twitter']
    notification_controller = NotificationController(db)
    print(notification_controller.delete_keyphrase())
    print(notification_controller.get_all_keyphrases())

# test_notification_controller()