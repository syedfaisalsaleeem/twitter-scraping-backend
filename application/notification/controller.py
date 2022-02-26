from datetime import timedelta
from datetime import datetime
from datetime import date
from bson.objectid import ObjectId

class NotificationController():
    def __init__(self,db) -> None:
        self.db = db
        self.collection = self.db['notification']
        self.limit = 50

    def get_all_keyphrases(self,status):
        try:
            resp = {}
            twitter_keyphrase_list = list()
            for i in self.collection.find({"status":status},{} , sort=[( "_id", -1 )]):
                i['_id'] = str(i['_id'])
                twitter_keyphrase_list.append(i)
            resp['data'] = twitter_keyphrase_list
            return resp,200
        except Exception as e:
            return str(e),500

    def total_records(self):
        return self.collection.count_documents({})

    def insert_records(self):
        for i in range(5):
            data = {
            "status":"completed",
            "key_phrase":"freekick",
            "start_date":"2022-02-24"
            }
            self.collection.insert_one(data)
        return "records inserted"

    def delete_keyphrase(self):
        records_length = self.total_records()
        if records_length > self.limit:
            total_records_delete = records_length - self.limit
            for i in self.collection.find({"status":"completed"},{"key_phrase":1,"start_date":1,"status":1}, sort=[( "_id", 1 )]).limit(total_records_delete):
                self.collection.delete_one({"_id":ObjectId(i['_id'])})
        else:
            return "less records"
        return "successfully removed"


def test_notification_controller():
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['twitter']
    notification_controller = NotificationController(db)
    print(notification_controller.total_records())
    print(notification_controller.delete_keyphrase())
    if notification_controller.delete_keyphrase() == "less records":
        print(notification_controller.insert_records())
    print(notification_controller.delete_keyphrase())
    print(notification_controller.total_records())
    # print(notification_controller.get_all_keyphrases(status="pending"))

# test_notification_controller()