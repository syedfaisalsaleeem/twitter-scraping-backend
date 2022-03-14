import unittest
from control_cronjob_controller import ControlCronJobController

class TestCronJobController(unittest.TestCase):

    def test_insert_cronjob_keyphrase(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['twitter']
        cronjob_controller = ControlCronJobController(db)
        response = cronjob_controller.insert()
        self.assertAlmostEqual(response[1], 201)
        response = cronjob_controller.insert()
        self.assertAlmostEqual(response[1], 409)
        response = cronjob_controller.delete()
        self.assertAlmostEqual(response[1], 204)

    def test_update_cronjob_keyphrase(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['twitter']
        cronjob_controller = ControlCronJobController(db)
        response = cronjob_controller.insert()
        self.assertAlmostEqual(response[1], 201)
        response = cronjob_controller.update(False)
        self.assertAlmostEqual(response[1], 204)
        response = cronjob_controller.delete()
        self.assertAlmostEqual(response[1], 204)