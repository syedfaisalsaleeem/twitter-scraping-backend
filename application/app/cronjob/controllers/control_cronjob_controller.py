class ControlCronJobController():
    '''
        This class is for cron job keywords scrapping
    '''
    def __init__(self, db) -> None:
        self.collection = db['controlcronjob']

    def get(self):
        try:
            resp = {}
            resp['data'] = self.collection.find_one({},{"_id":0})
            return resp,200
        except Exception as e:
            return str(e),500

    def insert(self):
        try:
            resp = {}
            data = {"startcronjob": True}
            if self.collection.find_one({"startcronjob": True},{}):
                resp['data'] = "record exsists"
                return resp,409
            self.collection.insert_one(data)
            resp['data'] = "records inserted"
            return resp,201
        except Exception as e:
            return str(e),500

    def update(self, status):
        try:
            resp = {}
            data = {"startcronjob": status}
            self.collection.update_one({}, {"$set": data})
            resp['data'] = "records updated"
            return resp,204
        except Exception as e:
            return str(e),500

    def delete(self):
        try:
            resp = {}
            self.collection.delete_one({})
            resp['data'] = "successfully removed"
            return resp,204
        except Exception as e:
            return str(e),500