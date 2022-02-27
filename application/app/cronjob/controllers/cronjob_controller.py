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
        
