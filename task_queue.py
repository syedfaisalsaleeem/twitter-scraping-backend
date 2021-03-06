from celery import Celery, signals
from app import app
from application.app.cronjob.controllers.control_cronjob_controller import ControlCronJobController
from controller import Controller
from application.app.twitter.cronjob_twitter_scraping_controller import CronJobTwitterScrapingController
from application.app.cronjob.controllers.cronjob_controller import CronJobTime
from celery.schedules import crontab
from app import minutes
import os
from dotenv import load_dotenv

load_dotenv()
celery = Celery("tasks",  broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    beat_schedule={
      "scrapped_keywords_in_twitter": {
          "task": "task_queue.scrapped_keywords_in_twitter",
          # Run every second
          "schedule": crontab(minute=minutes),
      }
  },
)

@celery.task()
def twitter_scraping(**kwargs):
    from pymongo import MongoClient
    client = MongoClient(os.getenv('MONGO_URI'))
    db_twitter = client['twitter']
    query = kwargs['query']
    try:
        Controller(query[0],query[1],query[2],query[3],query[4],db_twitter).start()
    except Exception as e:
        print(e)


@celery.task()
def scrapped_keywords_in_twitter():
    try:
        from pymongo import MongoClient
        client = MongoClient(os.getenv('MONGO_URI'))
        db_twitter = client['twitter']
        response = ControlCronJobController(db_twitter).get()
        response = response[0]['data']["startcronjob"]
        if response:
            method="cronjob"
            cronjob_controller = CronJobTime(db_twitter)
            response = cronjob_controller.update_cronjobtime()
            CronJobTwitterScrapingController([],'','',method,False,db_twitter).start()
            print("------ starting keywords scrapping ------------------")
        else:
            print("------ StartCronJob is not allowed -------------")
    except Exception as e:
        print("----- error in keywords scrapping ----", e)

@celery.task
def timer():
    print("timer is on")