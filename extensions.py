import os

from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from prometheus_flask_exporter import PrometheusMetrics

# DATABASE
def make_db(app):
    # SQL
    db = SQLAlchemy()
    MYSQL_PASSWORD = app.config.get("MYSQL_PASSWORD")
    MYSQL_STRING = f"mysql://shadja:{MYSQL_PASSWORD}@localhost/shadja_dev"
    app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_STRING
    db.init_app(app)

    # Mongo
    mg = PyMongo()
    mg.init_app(app)

    # CORS
    CORS(app)
    return db, mg, app

# CELERY AND RABBITMQ
def make_celery(app):
    RABBITMQ_PASSWORD = app.config.get('RABBITMQ_PASSWORD')
    CELERY_BROKER_URL_BUILT = f'amqp://shadja:{RABBITMQ_PASSWORD}@localhost:5672/shadjavhost'

    celery = Celery(
        app.import_name,
        broker=CELERY_BROKER_URL_BUILT
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# PROMETHEUS
metrics = PrometheusMetrics.for_app_factory()
