import unittest
from controller import NotificationController
class TestNotificationController(unittest.TestCase):
    def test_update_records(self):
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017/')
        db = client['twitter']
        notification_controller = NotificationController(db)
        response = notification_controller.update_keyphrase("scraped")
        self.assertAlmostEqual(response[1], 200)
        self.assertAlmostEqual(response[0]['data'], "successfully updated")