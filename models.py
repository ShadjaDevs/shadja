import json
from sqlalchemy_utils import UUIDType
import uuid

from shadja import db, mg

'''
Contains all models
'''

subscription_pincode = db.Table('subscriptions_pincodes',
    db.Column('subscription_id', db.Integer, db.ForeignKey('subscriptions.id')),
    db.Column('pincode_code', db.Integer, db.ForeignKey('pincodes.code'))
)

class Pincode(db.Model):
    __tablename__ = 'pincodes'
    '''Class to represent every new pincode added to system by users'''
    code = db.Column(db.Integer, primary_key=True)
    availabilities = db.Column(db.JSON)
    # hash of all availabilities, using Session.hash_many()
    availabilities_hash = db.Column(db.String(24))
    subscriptions = db.relationship(
        "Subscription", 
        secondary=subscription_pincode,
        lazy=True, 
        backref=db.backref("pincodes", lazy=True))

    def __init__(self, code, availabilities=json.dumps({})):
        self.code = code
        self.availabilities = availabilities

    def __repr__(self):
        return f'Pin<{self.code}>'


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    '''Class object to represent every new _request_ added to the system by users'''
    id = db.Column(db.Integer, primary_key=True)
    old = db.Column(db.Boolean)
    want_free = db.Column(db.Boolean)
    flavor = db.Column(db.String(32))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    email = db.Column(db.String(128))
    mobile = db.Column(db.String(15))
    telegram_id = db.Column(db.String(128))
    send_email = db.Column(db.Boolean)
    send_mobile = db.Column(db.Boolean)
    send_telegram = db.Column(db.Boolean)
    verified_email = db.Column(db.Boolean)
    verified_mobile = db.Column(db.Boolean)
    verified_telegram = db.Column(db.Boolean)
    otp_email = db.Column(db.String(64))
    otp_mobile = db.Column(db.String(64))
    otp_telegram = db.Column(db.String(64))
    # UUID for tracking OTPs
    uuid = db.Column(UUIDType(binary=True))
    # hash of all sessions included in notification using Session.hash_many()
    notification_hash = db.Column(db.String(24))

    def __init__(self, old, pincodes):
        self.old = old
        self.pincodes = list(Pincode(code) for code in pincodes)
        self.uuid = uuid.uuid4()

    def __repr__(self):
        return f'Subscription<old:{self.old} want_free:{self.want_free} flavor:{self.flavor}>'
