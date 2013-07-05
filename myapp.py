from flask import Flask
from celery import Celery

app = Flask('myapp')
celery = Celery('myapp')
celery.conf.add_defaults(app.config)

@celery.task
def hello():
    with app.test_request_context() as request:
        print('Hello {0!r}.format(request))
