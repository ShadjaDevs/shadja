import os

from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from prometheus_flask_exporter import PrometheusMetrics

# DATABASE
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_STRING = f"mysql://shadja:{MYSQL_PASSWORD}@localhost/shadja_dev"
db = SQLAlchemy()

def make_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_STRING
    db.init_app(app)
    return db, app

# CELERY AND RABBITMQ
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD')
CELERY_BROKER_URL_BUILT = f'amqp://shadja:{RABBITMQ_PASSWORD}@localhost:5672/shadjavhost'

def make_celery(app):
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
