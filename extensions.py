import os

from flask_sqlalchemy import SQLAlchemy

MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_STRING = f"mysql://shadja:{MYSQL_PASSWORD}@localhost/shadja_dev"

db = SQLAlchemy()
