import os 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_STRING = f"mysql://shadja:{MYSQL_PASSWORD}@localhost/shadja_dev"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_STRING
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from models import *

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello there!</h1>"

if __name__=="__main__":
    app.run(host="0.0.0.0")