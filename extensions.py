import os

from flask_sqlalchemy import SQLAlchemy
from celery import Celery

def sqlalchemy_setup(app):
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_STRING = f"mysql://shadja:{MYSQL_PASSWORD}@localhost/shadja_dev"

    app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_STRING
    db = SQLAlchemy(app)
    return db, app 

def celery_setup(app):
    RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
    app.config['CELERY_BROKER_URL'] = f'amqp://shadja:{RABBITMQ_PASSWORD}@localhost:5672/shadjavhost'

    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery, app
