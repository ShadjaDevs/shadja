import datetime
from flask import Flask, render_template, request
from flask_migrate import Migrate
import uuid

from extensions import make_db, metrics, make_celery
import utils

app = Flask(__name__)
app.config.from_envvar('SHADJA_SETTINGS')

# set up database
db, app = make_db(app)
migrate = Migrate(app, db)
from models import *

# other extensions
celery = make_celery(app)
metrics.init_app(app)

# Status codes used
SuccessCode = 200
FailureCode = 400

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/update_subscription/<uid>', methods=['POST'])
@app.route('/add_subscription', methods=['POST'])
def add_subscription(uid=None):
    '''End point to be used by front end to post form data.
    Can also be used by third party clients to add new subscriptions'''

    resp_json = {}
    resp_json['success'] = False

    if not request.is_json:
        resp_json['error'] = 'No JSON payload found'
        return resp_json, FailureCode

    in_json = request.get_json()

    required_keys = ['old', 'pincodes']
    optional_keys = ['want_free', 'flavor', 'start_date', 'end_date']
    notify_channel = ['email', 'mobile', 'telegram_id']

    # Check if bare minimum entries are ready
    if not all(x in in_json for x in required_keys):
        resp_json['error'] = 'One or more required fields missing'
        return resp_json, FailureCode

    # Need at least one way to notify the subscriber
    if not any(x in in_json for x in notify_channel):
        resp_json['error'] = 'Specify at least one notification channel'
        return resp_json, FailureCode

    # Ensure values are the right type
    type_dict = {
        'old': bool,
        'pincodes': list,
        'want_free': bool,
        'flavor': str,
        'start_date': datetime.datetime,
        'end_date': datetime.datetime,
        'email': str,
        'mobile': int,
        'telegram_id': str
    }

    if not all((v is None) or isinstance(v, type_dict[k]) for k,v in in_json.items()):
        resp_json['error'] = 'One or more fields have the wrong type'
        return resp_json, FailureCode

    # TODO: Need more checks for specific inputs like email, phone, pincodes etc.

    if uid is None:
        subscription = Subscription(old=in_json.get('old'))
    else:
        subscription = Subscription.query.filter(Subscription.uuid==uuid.UUID(uid)).first()

    # FIXME: Is this correct way to assign the pincodes?
    subscription.pincodes = list(Pincode(code) for code in in_json.get('pincodes'))
    subscription.want_free = in_json.get('want_free')
    subscription.flavor = in_json.get('flavor')
    subscription.start_date = in_json.get('start_date')
    subscription.end_date = in_json.get('end_date')
    subscription.email = in_json.get('email')
    subscription.mobile = in_json.get('mobile')
    subscription.telegram_id = in_json.get('telegram_id')
    subscription.send_email = 'email' in in_json
    subscription.send_mobile = 'mobile' in in_json
    subscription.send_telegram = 'telegram_id' in in_json

    if in_json.get('mobile'):
        otp, key = utils.get_otp_hash()
        subscription.otp_mobile = key
        # TODO: Send otp as SMS
    if in_json.get('email'):
        otp, key = utils.get_otp_hash()
        subscription.otp_email = key
        notify.send_otp_email(subscription, otp)

    if uid is None:
        db.session.add(subscription)
    db.session.commit()

    resp_json['uuid'] = subscription.uuid
    resp_json['success'] = True

    # # FIXME: Can use this OTP always to login, why anything new?
    return resp_json, SuccessCode

@app.route('/input_otp/<uid>', methods=['POST'])
def input_otp(uid):
    '''
    Endpoint used to post OTP
    '''

    resp_json = {}
    resp_json['success'] = False

    if not request.is_json:
        resp_json['error'] = 'No JSON payload found'
        return resp_json, FailureCode

    subscription = Subscription.query.filter(Subscription.uuid==uuid.UUID(uid)).first()
    
    if not subscription:
        resp_json['error'] = f'Subscriber with uid={uid} not found'
        return resp_json, FailureCode

    in_json = request.get_json()
    resp_json['success'] = True

    # Hash compares
    if subscription.send_email and (not subscription.verified_email):
        if 'otp_email' not in in_json:
            resp_json['success'] = False
            resp_json['error'] = 'Specify email OTP'
            return resp_json, FailureCode
        resp_json['verified_email'] = subscription.verified_email = subscription.otp_email==in_json.get('otp_email')
        resp_json['success'] = resp_json['success'] and subscription.verified_email
    db.session.commit()

    if subscription.send_mobile and (not subscription.verified_mobile):
        if 'otp_mobile' not in in_json:
            resp_json['success'] = False
            resp_json['error'] = 'Specify mobile OTP'
            return resp_json, FailureCode
        resp_json['verified_mobile'] = subscription.verified_mobile = subscription.otp_mobile==in_json.get('otp_mobile')
        resp_json['success'] = resp_json['success'] and subscription.verified_mobile

    db.session.commit()
    return resp_json, SuccessCode

@app.route('/remove_subscription/<uid>', methods=['DELETE'])
def remove_subscription(uid):
    '''
    Endpoint used to remove a subscription from the db
    '''

    resp_json = {}
    resp_json['success'] = False

    subscription = Subscription.query.filter(Subscription.uuid==uuid.UUID(uid)).first()

    if not subscription:
        resp_json['error'] = f'Subscriber with uid={uid} not found'
        return resp_json, FailureCode

    db.session.delete(subscription)
    db.session.commit()
    resp_json['success'] = True
    return resp_json, SuccessCode

@app.route('/nearby_codes/<pincode>/<radius>', methods=['GET'])
def nearby_codes(pincode, radius):
    '''
    Endpoint used to post OTP
    '''

    resp_json = {}
    resp_json['success'] = False

    if not (pincode.isdigit() and (100000 <= pincode <= 999999)):
        resp_json['error'] = 'Specify a valid pincode'
        return resp_json, FailureCode

    resp_json[pincode] = []

    resp_json['success'] = True
    return resp_json, SuccessCode

if __name__=="__main__":
    app.run(host="0.0.0.0")
