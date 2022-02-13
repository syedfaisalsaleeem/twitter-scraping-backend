from celery import Celery, signals
from app import app
from controller import Controller


celery = Celery("tasks",  broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task()
def twitter_scraping(**kwargs):
    query = kwargs['query']
    try:
        Controller(query[0],query[1],query[2],query[3],query[4]).start()
    except Exception as e:
        print(e)