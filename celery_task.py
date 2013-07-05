from celery import Celery

celery = Celery('celery_task', broker='amqp://guest@localhost//')

@celery.task
def add(x, y):
    return x + y

