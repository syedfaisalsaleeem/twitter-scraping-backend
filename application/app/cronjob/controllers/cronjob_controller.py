from bson.objectid import ObjectId
class CronJobController():
    '''
        This class is for cron job keywords scrapping
    '''
    def __init__(self, db) -> None:
        self.collection = db['cronjobkeywords']

    def get_all_cronjob_key_phrases(self, method) -> list:
        '''
            This function is used when we start cron job scrapping
        '''
        twitter_keyphrase_list = list()
        for i in self.collection.find({"method":method},{} , sort=[( "_id", -1 )]):
            i['_id'] = str(i['_id'])
            twitter_keyphrase_list.append(i)

        return twitter_keyphrase_list

    def get_all_keyphrases(self,method):
        try:
            resp = {}
            resp['data'] = self.get_all_cronjob_key_phrases(method)
            return resp,200
        except Exception as e:
            return str(e),500

    def insert_cronjob_keyphrase(self, keywords):
        # keywords wii be a list of keywords
        try:
            resp = {}
            for value in keywords:
                data = {"key_phrase": value, "method": "cronjob", "status": "pending"}
                self.collection.insert_one(data)
            resp['data'] = "records inserted"
            return resp,201

        except Exception as e:
            return str(e),500

    def delete_cronjob_keyphrase(self, delete_id):
        try:
            resp = {}
            self.collection.delete_one({"_id":ObjectId(delete_id)})
            resp['data'] = "successfully removed"
            return resp,204
        except Exception as e:
            return str(e),500

    def update_status(self,id,data):
        try:
            resp = {}
            self.collection.update_one({"_id": ObjectId(id)}, {"$set":{"status":data}})
            resp['data'] = "successfully updated"
            return resp,204
        except Exception as e:
            return str(e),500

    def update_location(self,id,status,stored_place):
        try:
            resp = {}
            self.collection.update_one({"_id": ObjectId(id)}, {"$set":{"status":status,"location":stored_place}})
            resp['data'] = "successfully updated"
            return resp,204
        except Exception as e:
            return str(e),500
        
class CronJobTime():
    def __init__(self, db) -> None:
        self.collection = db['cronjobtime']

    def insert_cronjob_time(self):
        # keywords wii be a list of keywords
        try:
            from datetime import datetime
            from pytz import timezone
            resp = {}
            current_time = datetime.now(timezone('UTC'))
            current_time = current_time.replace(tzinfo=None)
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            if self.get_cronjobtime()[0]['data'] != None:
                resp['data'] = "record exsists"
                return resp,409
            data = {"cronjobtime": str(current_time)}
            self.collection.insert_one(data)
            resp['data'] = "records inserted"
            return resp,201

        except Exception as e:
            return str(e),500


    def update_cronjobtime(self):
        try:
            from datetime import datetime
            from pytz import timezone
            resp = {}
            next_cronjob_time = datetime.now(timezone('UTC'))
            next_cronjob_time = next_cronjob_time.replace(tzinfo=None)
            next_cronjob_time = next_cronjob_time.strftime("%Y-%m-%d %H:%M:%S")
            self.collection.update_one({}, {"$set":{"cronjobtime":str(next_cronjob_time)}})
            resp['data'] = "successfully updated"
            return resp,204
        except Exception as e:
            return str(e),500

    def get_cronjobtime(self):
        try:
            resp = {}
            resp['data'] = self.collection.find_one({},{"_id":0})
            return resp,200
        except Exception as e:
            return str(e),500

    
    def get_hours_remaining(self,next_cronjob_time):
        try:
            from datetime import datetime
            from datetime import timedelta
            from dateutil.relativedelta import relativedelta
            import pytz
            from pytz import timezone
            current_time = datetime.now(timezone('UTC'))
            current_time = current_time.replace(tzinfo=None)
            next_cronjob_time = datetime.strptime(next_cronjob_time, '%Y-%m-%d %H:%M:%S')
            next_cronjob_time = next_cronjob_time.replace(tzinfo=None)
            delta = next_cronjob_time - current_time
            delta = delta.total_seconds()
            delta = int(delta)
            delta = delta/60
            return delta
        except Exception as e:
            return "error occured"
            
    def calculate_nextcronjobtime(self,minutes):
        try:
            resp = {}
            from datetime import datetime
            from datetime import timedelta
            from dateutil.relativedelta import relativedelta
            import pytz
            from pytz import timezone
            minutes = minutes.split("*/")[1]
            current_time = self.get_cronjobtime()[0]
            current_time = current_time['data']['cronjobtime']
            current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
            current_time = current_time.replace(tzinfo=None)
            next_cronjob_time = current_time + relativedelta(minutes=int(minutes))
            next_cronjob_time = next_cronjob_time.replace(tzinfo=None)
            next_cronjob_time = next_cronjob_time.strftime("%Y-%m-%d %H:%M:%S")
            minutes = self.get_hours_remaining(next_cronjob_time)
            resp['data'] = {
                "next_cronjob_time": next_cronjob_time,
                "minutes_remaining": minutes
            }
            return resp,200
        except Exception as e:
            print(str(e))
            return str(e),500