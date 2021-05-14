import datetime
import uuid

from flask import Flask, render_template, request
from flask_migrate import Migrate
from sqlalchemy import inspect

from extensions import make_db, metrics, make_celery
import utils

app = Flask(__name__)
app.config.from_envvar('SHADJA_SETTINGS')

# set up database
db, mg, app = make_db(app)
migrate = Migrate(app, db)
from models import *
import notify

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

    if not ((uid is None) or utils.isValidUUID(uid)):
        resp_json['error'] = 'Invalid UUID'
        return resp_json, FailureCode

    in_json = request.get_json()

    required_keys = ['old', 'pincodes']
    optional_keys = ['want_free', 'flavor', 'start_date', 'end_date']
    notify_channel = ['email', 'mobile', 'telegram_id']

    # Check if bare minimum entries are ready
    if not all(in_json.get(x) is not None for x in required_keys):
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
        'start_date': str,
        'end_date': str,
        'email': str,
        'mobile': int,
        'telegram_id': str
    }

    if not all((v is None) or isinstance(v, type_dict[k]) for k,v in in_json.items()):
        resp_json['error'] = 'One or more fields have the wrong type'
        return resp_json, FailureCode

    if not (
        all(utils.isValidPin(pin) for pin in in_json['pincodes']) and
        ((in_json.get('flavor') is None) or
            utils.isValidFlavor(in_json['flavor'])) and
        ((in_json.get('start_date') is None) or
            utils.isValidDateStr(in_json['start_date'])) and
        ((in_json.get('end_date') is None) or
            utils.isValidDateStr(in_json['end_date'])) and
        ((in_json.get('email') is None) or
            utils.isValidEmail(in_json['email'])) and
        ((in_json.get('mobile') is None) or
            utils.isValidMobile(in_json['mobile'])) and
        ((in_json.get('telegram_id') is None) or
            utils.isValidTelegramId(in_json['telegram_id']))):

        resp_json['error'] = 'One or more fields have wrong format'
        return resp_json, FailureCode

    if uid is None:
        subscription = Subscription(in_json.get('old'), in_json['pincodes'])
    else:
        subscription = Subscription.query.filter(
            Subscription.uuid==uuid.UUID(uid)).first()

        if not subscription:
            resp_json['error'] = f'Subscriber with uuid={uid} not found'
            return resp_json, FailureCode

        subscription.old = in_json.get('old')
        subscription.pincodes = create_pincodes(in_json['pincodes'])

    subscription.want_free = in_json.get('want_free')
    subscription.flavor = in_json.get('flavor')
    subscription.start_date = in_json.get('start_date')
    subscription.end_date = in_json.get('end_date')

    # Allow only adding new channels, cannot delete
    if (uid is None) or (not subscription.verified_email):
        subscription.email = in_json.get('email')
        subscription.send_email = 'email' in in_json
    if (uid is None) or (not subscription.verified_mobile):
        subscription.mobile = in_json.get('mobile')
        subscription.send_mobile = 'mobile' in in_json
    if (uid is None) or (not subscription.verified_telegram):
        subscription.telegram_id = in_json.get('telegram_id')
        subscription.send_telegram = 'telegram_id' in in_json

    if in_json.get('mobile') and (not subscription.verified_mobile):
        otp, key = utils.get_otp_hash()
        subscription.otp_mobile = key
        # TODO: Send otp as SMS
    if in_json.get('email') and (not subscription.verified_email):
        otp, key = utils.get_otp_hash()
        subscription.otp_email = key
        notify.send_otp_email(subscription, otp)

    if uid is None:
        db.session.add(subscription)
    db.session.commit()

    resp_json['uuid'] = subscription.uuid
    resp_json['success'] = True

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

    if not utils.isValidUUID(uid):
        resp_json['error'] = 'Invalid UUID'
        return resp_json, FailureCode

    subscription = Subscription.query.filter(
        Subscription.uuid==uuid.UUID(uid)).first()
    
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

        if not utils.isValidOTP(in_json['otp_email']):
            resp_json['success'] = False
            resp_json['error'] = 'Invalid OTP format'
            return resp_json, FailureCode

        subscription.verified_email = \
            subscription.otp_email==utils.get_hash(in_json.get('otp_email'))
        resp_json['verified_email'] = subscription.verified_email
        resp_json['success'] = resp_json['success'] and \
            subscription.verified_email
    db.session.commit()

    if subscription.send_mobile and (not subscription.verified_mobile):
        if 'otp_mobile' not in in_json:
            resp_json['success'] = False
            resp_json['error'] = 'Specify mobile OTP'
            return resp_json, FailureCode

        if not utils.isValidOTP(in_json['otp_mobile']):
            resp_json['success'] = False
            resp_json['error'] = 'Invalid OTP format'
            return resp_json, FailureCode

        subscription.verified_mobile = \
            subscription.otp_mobile==utils.get_hash(in_json.get('otp_mobile'))
        resp_json['verified_mobile'] = subscription.verified_mobile
        resp_json['success'] = resp_json['success'] and \
            subscription.verified_mobile

    db.session.commit()
    return resp_json, SuccessCode

@app.route('/get_subscription/<uid>', methods=['GET'])
def get_subscription(uid):
    '''
    Endpoint used to get a subscription from the db
    '''

    resp_json = {}
    resp_json['success'] = False

    if not utils.isValidUUID(uid):
        resp_json['error'] = 'Invalid UUID'
        return resp_json, FailureCode

    subscription = Subscription.query.filter(
        Subscription.uuid==uuid.UUID(uid)).first()

    if not subscription:
        resp_json['error'] = 'Subscriber with uuid not found'
        return resp_json, FailureCode

    # TODO: Populate out_json
    out_data =  { c.key: getattr(subscription, c.key)
        for c in inspect(subscription).mapper.column_attrs }

    remove_keys = [
        'id',
        'otp_email',
        'otp_mobile',
        'otp_telegram',
        'notification_hash'
    ]

    for key in remove_keys:
        del out_data[key]

    resp_json['subscription'] = out_data
    resp_json['success'] = True
    return resp_json, SuccessCode

@app.route('/remove_subscription/<uid>', methods=['GET'])
def remove_subscription(uid):
    '''
    Endpoint used to remove a subscription from the db
    '''

    resp_json = {}
    resp_json['success'] = False

    if not utils.isValidUUID(uid):
        resp_json['error'] = 'Invalid UUID'
        return resp_json, FailureCode

    subscription = Subscription.query.filter(
        Subscription.uuid==uuid.UUID(uid)).first()

    if not subscription:
        resp_json['error'] = 'Subscriber with uuid not found'
        return resp_json, FailureCode

    db.session.delete(subscription)
    db.session.commit()
    resp_json['success'] = True
    return resp_json, SuccessCode

@app.route('/nearby_pincodes/<pincode>/<radius>', methods=['GET'])
def nearby_codes(pincode, radius):
    '''
    Endpoint used to post OTP
    '''

    resp_json = {}
    resp_json['success'] = False

    if not (pincode.isdigit() and utils.isValidPin(int(pincode))):
        resp_json['error'] = 'Specify a valid pincode'
        return resp_json, FailureCode

    if not (radius.isdigit() and utils.isValidRadius(int(radius))):
        resp_json['error'] = 'Specify a valid radius'
        return resp_json, FailureCode

    pincode = int(pincode)
    entry = mg.db.nearby_pincodes.find_one({'key': pincode})

    # TODO: Maybe doing a blanket try-except will simplify this
    # But we run the risk of masking other errors.
    if not (
        (entry is not None) and
        isinstance(entry, dict) and
        ('value' in entry) and
        isinstance(entry['value'], dict) and
        (radius in entry['value']) and
        isinstance(entry['value'][radius],list)):

        resp_json['error'] = 'No entry found for this pincode-radius pair'
        return resp_json, FailureCode

    # Get all the pincodes lesser than or equal to this radius
    pincodes = list(
        codes for r, codes in entry['value'].items() if (int(r)<=int(radius)))
    resp_json['pincodes'] = sorted(
        code for codes in pincodes for code in codes)
    resp_json['success'] = True
    return resp_json, SuccessCode

if __name__=="__main__":
    app.run(host="0.0.0.0")
