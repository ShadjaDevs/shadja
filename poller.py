'''
Script to be called by the cron job periodically to query CoWIN and update subscribers
'''

import datetime
from collections import defaultdict
from celery import Celery

from models import Pincode, Subscription
from shadja import db
from sessions import *
import cowin
import notify

app = Celery('poller', broker='pyamqp://guest@localhost')

# Read the database to find which pincodes to query
def getAllPincodes():
    ''' Get a list of pincodes to query CoWIN'''
    return Pincode.query.all()

def getAllSubscriptions():
    '''Get a list of subscriptions to process with new data'''
    return Subscription.query.all()

def updateCoWINData(pincode):
    '''Get CoWIN data for given pincode and write to a database'''
    # TODO: Current implementation will give slots for next week. What about the dates in the future?
    data = cowin.findWeeklySessionsByPin(pincode.code)
    print(data)
    data_hashed = str(hash_calendar(data))
    if pincode.availabilities_hash != data_hashed:
        pincode.availabilities = data
        pincode.availabilities_hash = data_hashed
        db.session.add(pincode)
        db.session.commit()
        return True
    # no changes to calendar.
    return False

def processNotifications(subscription):
    '''Notify the subscriptions if there are new slots opening up'''

    # Define functions for this subscription
    def is_valid_center(center):
        if 'pincode' in center:

            return \
                (center['pincode'] in (p.code for p in subscription.pincodes)) and \
                ((subscription.want_free is None) or \
                    (subscription.want_free == (center['fee_type']=='Free')))
        return False

    def is_valid_session(session):
        session['date'] = datetime.datetime.strptime(session['date'], cowin.DateFormat).date()
        
        valid = ((subscription.start_date is None) and \
                (subscription.end_date is None)) or \
            (subscription.start_date.date() <= session['date'] <= subscription.end_date.date()) and \
            (int(session['available_capacity']) > 0) and \
            (subscription.old or (session['min_age_limit']==18)) and \
            ((subscription.flavor is None) or (subscription.flavor==session['vaccine'].lower()))
        return valid

    def is_valid_slot(slot):
        start_time, _, end_time = slot.partition('-')

        start_time = datetime.datetime.strptime(start_time, cowin.TimeFormat).time()
        end_time   = datetime.datetime.strptime(end_time, cowin.TimeFormat).time()

        # Need to find out if this slot has any overlap with the slot user is requesting
        # Interestingly, this is not trivial
        # https://stackoverflow.com/questions/3269434/whats-the-most-efficient-way-to-test-two-integer-ranges-for-overlap
        valid = ((subscription.start_time is None) and \
                (subscription.end_time is None)) or \
            ((subscription.start_time <= end_time) and \
             (subscription.end_time >= start_time))
        return valid

    # Find all valid slots in the pincodes
    available_centers = defaultdict(list)

    for pincode in subscription.pincodes:
        data = pincode.availabilities
        # At this moment, assuming no guarantees
        # about this JSON data. Hence, checking
        # for the key in JSON before trying to access it.
        # Look before you leap approach
        if data is None or 'centers' not in data:
            continue

        # First figure out if this customer is interested in
        # this center
        centers = list(filter(is_valid_center, data['centers']))

        for center in centers:
            if 'sessions' not in center:
                continue

            # Figure out if this customer is interested in
            # the dates offered
            sessions = list(filter(is_valid_session, center['sessions']))

            for session in sessions:
                if 'slots' not in session:
                    continue

                # Figure out if this custmer is interested in
                # the slots offered
                session['slots'] = list(filter(is_valid_slot, session['slots']))

            # Filter out sessions with no valid slots
            sessions = list(filter(lambda session: len(session['slots'])>0, sessions))
            if len(sessions) > 0:
                center['sessions'] = sessions
                available_centers[pincode].append(center)

    # Send the notification
    # TODO: If previously informed of the same, should you still do? May be yes
    if subscription.email:
        notify.notify_email(subscription, available_centers)

    # if subscription.mobile:
    #     notify_mobile(subscription, available_centers)

    # if subscription.telegram_id:
    #     notify_mobile(subscription, available_centers)

@app.task
def queryCoWIN(pincode):
    '''Query CoWIN and update consumers of any relevant slots'''
    # Get data from CoWIN for each of these pincodes and update internal DB
    pincode = Pincode.query.filter(Pincode.code==pincode).first()
    if pincode is None:
        print(f"Unknown pincode: {pincode}")
        return

    if updateCoWINData(pincode):
        # Now, update the consumers if there are any relevant slots for them
        for subscription in Subscription.query.join(
                                Pincode, 
                                Subscription.pincodes, 
                                aliased=True
            ).filter(
                Pincode.code == pincode.code
            ):
            processNotifications(subscription)

@app.task
def refreshAllPINs():
    for pincode in Pincode.query.all():
        queryCoWIN.delay(pincode.code)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3, refreshAllPINs.s(), name='Refresh all pins')

if __name__=='__main__':
    queryCoWIN(560008)
