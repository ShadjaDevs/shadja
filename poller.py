'''
Script to be called by the cron job periodically to query CoWIN and update subscribers
'''

import datetime
from collections import defaultdict

from sessions import *
import cowin
import notify
import utils
from shadja import celery, db
from models import Pincode, Subscription

# Read the database to find which pincodes to query
def getAllPincodes():
    ''' Get a list of pincodes to query CoWIN'''
    return Pincode.query.all()

def getAllSubscriptions():
    '''Get a list of subscriptions to process with new data'''
    return Subscription.query.all()

def updateCoWINData(pincode):
    '''Get CoWIN data for given pincode and write to a database'''
    # TODO: Current implementation will give slots for next week.
    # What about the dates in the future?
    data = cowin.findWeeklySessionsByPin(pincode.code)
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
    def is_valid_subscriber(subscription):
        return (subscription.verified_telegram or
            subscription.verified_mobile or
            subscription.verified_email)

    '''Notify the subscriptions if there are new slots opening up'''

    # Define functions for this subscription
    def is_valid_center(center):
        if 'pincode' in center:

            return \
                (center['pincode'] in (p.code for p in subscription.pincodes)) and \
                ((subscription.want_free is None) or \
                    (subscription.want_free == (center['fee_type']=='Free')))
        return False

    def is_valid_date(session_date):
        '''Check if the date of this session is ok for this subscriber'''
        start_ok = ((subscription.start_date is None) or
            (session_date >= subscription.start_date))

        end_ok = ((subscription.end_date is None) or
            (session_date <= subscription.end_date))

        return start_ok and end_ok

    def is_valid_session(session):
        '''Session is ok only if there are non-zero slots and the session
        is within the preferences given by the subscriber'''
        session_date = datetime.datetime.strptime(
            session['date'], utils.DateFormat).date()
        
        valid = is_valid_date(subscription, session_date) and \
            (int(session['available_capacity']) > 0) and \
            (subscription.old or (session['min_age_limit']==18)) and \
            ((subscription.flavor is None) or (subscription.flavor==session['vaccine'].lower()))
        return valid

    def is_valid_slot(slot):
        start_time, _, end_time = slot.partition('-')

        start_time = datetime.datetime.strptime(
            start_time,
            utils.TimeFormat
        ).time()

        end_time = datetime.datetime.strptime(
            end_time,
            utils.TimeFormat
        ).time()

        # Need to find out if this slot has any overlap with the slot user is requesting
        # Interestingly, this is not trivial
        # https://stackoverflow.com/questions/3269434/whats-the-most-efficient-way-to-test-two-integer-ranges-for-overlap
        valid = ((subscription.start_time is None) and \
                (subscription.end_time is None)) or \
            ((subscription.start_time <= end_time) and \
             (subscription.end_time >= start_time))
        return valid
    
    if not is_valid_subscriber(subscription):
        return

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

                # Figure out if this customer is interested in
                # the slots offered
                session['slots'] = list(filter(
                    is_valid_slot, session['slots']))

            # Filter out sessions with no valid slots
            sessions = list(filter(
                lambda session: len(session['slots'])>0, sessions))

            if len(sessions) > 0:
                center['sessions'] = sessions
                available_centers[pincode.code].append(center)

    # Send the notification
    # if new notification is same as the last one sent, then don't send
    # if there are no available centers, also don't send
    new_notification_hash = session.hash_calendars(available_centers)
    if ((not available_centers) or
        (new_notification_hash == subscription.notification_hash)):

        return

    sent_e, sent_m, sent_t = False, False, False
    if subscription.email and subscription.verified_email:
        sent_e = notify.notify_email(subscription, available_centers)

    if consumer.mobile and subscription.verified_mobile:
        sent_m = notify.notify_mobile(consumer, available_centers)

    if consumer.telegram_id and subscription.verified_telegram:
        sent_t = notify.notify_telegram(consumer, available_centers)

    if sent_e or sent_m or sent_t:
        subscription.notification_hash = new_notification_hash
        db.session.commit()

@celery.task
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

@celery.task
def refreshAllPINs():
    for pincode in Pincode.query.all():
        if len(pincode.subscriptions) > 0:
            queryCoWIN.delay(pincode.code)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        900, # 30s
        refreshAllPINs.s(),
        name='Refresh all pins'
    )

if __name__=='__main__':
    # queryCoWIN.delay(560008)
    pass
