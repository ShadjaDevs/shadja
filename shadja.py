import os
import hashlib
import random

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import Pincode, Subscription
import utils

MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_STRING = f"mysql://shadja:{MYSQL_PASSWORD}@localhost/shadja_dev"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_STRING
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import *

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/add_subscription', methods=['POST'])
def add_subscription():
    '''End point to be used by front end to post form data.
    Can also be used by third party clients to add new subscriptions'''
    data = request.get_json()

    # TODO: Some input checking needed?
    # TODO: Add a new entry to db
    subscription = Subscription(old=True, want_free=None, flavor=None)

    if mobile:
        otp, key = utils.get_otp_hash()
        subscription.otp_mobile = key
        # TODO: Send otp as SMS
    if email:
        otp, key = utils.get_otp_hash()
        subscription.otp_email = key
        # TODO: Send otp as email

    db.session.add(subscription)
    db.session.commit()

    # TODO: Get the primary key of the newly added entry and pass it on as the token
    id = 0
    # FIXME: Can use this OTP always to login, why anything new?
    return redirect(url_for('input_otp', id=id))

@app.route('/input_otp/<id>', methods=['GET', 'POST'])
def input_otp(id):
    success = None

    mobile, email = True, True # TODO: Get this from the db for the given id
    if request.method == 'POST':
        data = request.get_json()

        subscription = Subscription.query.filter(Subscription.id==id).first()

        # Check if OTP (hash) matches what was sent out
        success = ((not subscription.send_email) or (subscription.otp_email==data.get('email'))) and \
            ((not subscription.send_mobile) or (subscription.otp_mobile==data.get('mobile')))

        # Update entry in DB with email,phone verified
        if success:
            subscription.verified_email = True
            subscription.verified_mobile = True

    return render_template('input_otp.html', mobile=mobile, email=email, success=success)

if __name__=="__main__":
    app.run(host="0.0.0.0")