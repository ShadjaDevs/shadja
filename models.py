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
        'Subscription', 
        secondary=subscription_pincode,
        lazy=True, 
        backref=db.backref('pincodes', lazy=True))

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
    notifications = db.relationship('Notification', backref='subscription', lazy=True)

    def __init__(self, old, pincodes):
        self.old = old
        self.uuid = uuid.uuid4()

        # Create Pincode instances if they do not exist
        self.pincodes = create_pincodes(pincodes)
        # Make sure nothing was missed
        assert(len(self.pincodes)==len(pincodes))

    def __repr__(self):
        return f'Subscription<old:{self.old} want_free:{self.want_free} flavor:{self.flavor}>'

class Notification(db.Model):
    __tablename__ = 'notifications'
    '''Class object to represent hash of every session notification sent
    by the system to subscribers'''
    id = db.Column(db.Integer, primary_key=True)
    hsh = db.Column(db.String(24))
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'))

    def __init__(self, hsh):
        self.hsh = hsh

    def __repr__(self):
        return f'Notification<hash:{self.hsh}>'

def create_pincodes(pincodes):
    '''
    Create a pincode only if it does not exist already
    http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    '''
    instances = Pincode.query.filter(Pincode.code.in_(pincodes)).all()

    missing_pincodes = set(pincodes) - set(x.code for x in instances)

    for pincode in missing_pincodes:
        instance = Pincode(pincode)
        try:
            db.session.add(instance)
            db.session.commit()
        except IntegrityError:
            # This is when another thread created the same pincode
            db.session.rollback()
            instance = Pincode.query.filter(Pincode.code==pincode).first()
        instances.append(instance)
    return instances
