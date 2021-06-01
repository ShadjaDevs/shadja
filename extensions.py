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
    db.init_app(app)

    # Mongo
    mg = PyMongo()
    mg.init_app(app)

    # CORS
    CORS(app)
    return db, mg, app

# CELERY AND RABBITMQ
def make_celery(app):
    celery = Celery(config_source=app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# PROMETHEUS
metrics = PrometheusMetrics.for_app_factory()
