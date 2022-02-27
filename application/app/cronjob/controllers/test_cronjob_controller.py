import unittest
from cronjob_controller import CronJobController

class TestCronJobController(unittest.TestCase):

    def test_insert_cronjob_keyphrase(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['twitter']
        cronjob_controller = CronJobController(db)
        response = cronjob_controller.insert_cronjob_keyphrase(['1','2','3'])
        self.assertAlmostEqual(response[1], 201)
        self.assertAlmostEqual(response[0]['data'], "records inserted")
        for ids in cronjob_controller.get_all_cronjob_key_phrases(method="cronjob"):
            response = cronjob_controller.delete_cronjob_keyphrase(ids.get('_id'))
            self.assertAlmostEqual(response[1], 204)
            self.assertAlmostEqual(response[0]['data'], "successfully removed")

    def test_get_cronjob_keyphrase(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['twitter']
        cronjob_controller = CronJobController(db)
        cronjob_controller.insert_cronjob_keyphrase(['1','2','3'])
        response = cronjob_controller.get_all_keyphrases('cronjob')
        self.assertAlmostEqual(response[1], 200)
        self.assertAlmostEqual(response[0]['data'][0]['key_phrase'], '3')
        for ids in cronjob_controller.get_all_cronjob_key_phrases(method="cronjob"):
            response = cronjob_controller.delete_cronjob_keyphrase(ids.get('_id'))
            self.assertAlmostEqual(response[1], 204)
            self.assertAlmostEqual(response[0]['data'], "successfully removed")

    def test_delete_cronjob_keyphrase(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['twitter']
        cronjob_controller = CronJobController(db)
        cronjob_controller.insert_cronjob_keyphrase(['1','2','3'])
        for ids in cronjob_controller.get_all_cronjob_key_phrases(method="cronjob"):
            response = cronjob_controller.delete_cronjob_keyphrase(ids.get('_id'))
            self.assertAlmostEqual(response[1], 204)
            self.assertAlmostEqual(response[0]['data'], "successfully removed")