import json

from shadja import db
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
    subscrptions = db.relationship(
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
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    email = db.Column(db.String(128))
    mobile = db.Column(db.String(15))
    telegram_id = db.Column(db.String(128))
    send_email = db.Column(db.Boolean)
    send_mobile = db.Column(db.Boolean)
    send_telegram = db.Column(db.Boolean)
    # hash of all sessions included in notificaion using Session.hash_many()
    notification_hash = db.Column(db.String(24))

    def __init__(self, old, want_free, flavor):
        self.old = old
        self.want_free = want_free
        self.flavor = flavor

    def __repr__(self):
        return f'Subscription<old:{self.old} want_free:{self.want_free} flavor:{self.flavor}>'
