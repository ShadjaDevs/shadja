'''
Script to be called by the cron job periodically to query CoWIN and update subscribers
'''

import datetime
from collections import defaultdict
from copy import deepcopy
from celery import group, subtask

from sessions import *
import cowin
import notify
import utils
from shadja import celery, db
from models import Pincode, Subscription, Notification

def processNotifications(subscription):
    '''Figure out if slots are relevant to this susbscriber and notify if yes'''

    def is_valid_subscriber(subscription):
        '''Notify only if at least one notification channel is setup'''
        return (subscription.verified_telegram or
            subscription.verified_mobile or
            subscription.verified_email)

    # Define functions for this subscription
    def is_valid_center(center):
        '''Center is valid only if pincode and "free" preference matches'''
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
        
        valid = is_valid_date(session_date) and \
            (int(session['available_capacity']) > 0) and \
            (subscription.old or (session['min_age_limit']==18)) and \
            ((subscription.flavor is None) or (subscription.flavor==session['vaccine'].lower()))
        return valid

    def is_valid_slot(slot):
        '''Find out if this slot has any overlap with the user's time preference'''
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

    def is_new_session(session, center_id):
        return (str(hash_session(session, center_id)) not in
            (notif.hsh for notif in subscription.notifications))

    if not is_valid_subscriber(subscription):
        return False

    # Find all valid slots in the pincodes
    available_centers = defaultdict(list)

    for pincode in subscription.pincodes:
        data = deepcopy(pincode.availabilities)
        # At this moment, assuming no guarantees
        # about this JSON data. Hence, checking
        # for the key in JSON before trying to access it.
        # Look before you leap approach
        if not (data and data.get('centers')):
            continue

        # First figure out if this customer is interested in
        # this center
        data['centers'] = list(filter(is_valid_center, data['centers']))

        for center in data['centers']:
            if not center.get('sessions'):
                continue

            # Figure out if this customer is interested in
            # the dates offered
            center['sessions'] = list(
                filter(is_valid_session, center['sessions']))
            for session in center['sessions']:
                if not session.get('slots'):
                    continue

                # Figure out if this customer is interested in
                # the slots offered
                session['slots'] = list(filter(
                    is_valid_slot, session['slots']))

            # Filter out sessions with no valid slots
            center['sessions'] = list(filter(
                lambda session: len(session['slots'])>0, center['sessions']))

            # Filter out sessions already sent
            center_id = center.get('center_id')
            center['sessions'] = list(filter(
                lambda s: is_new_session(s, center_id), center['sessions']))

            if len(center['sessions'])>0:
                available_centers[pincode.code].append(center)

    # If there are no available centers, don't send any notification
    if not available_centers:
        return False

    # Send the notification
    sent_e, sent_m, sent_t = False, False, False
    if subscription.email and subscription.verified_email:
        sent_e = notify.notify_email(subscription, available_centers)

    if subscription.mobile and subscription.verified_mobile:
        sent_m = notify.notify_mobile(subscription, available_centers)

    if subscription.telegram_id and subscription.verified_telegram:
        sent_t = notify.notify_telegram(subscription, available_centers)

    if sent_e or sent_m or sent_t:
        for centers in available_centers.values():
            for center in centers:
                center_id = center.get('center_id')
                for session in center['sessions']:
                    subscription.notifications.append(
                        Notification(str(hash_session(session, center_id))))
        db.session.commit()
        return True

    return False

@celery.task
def updatePincode(code):
    '''Get CoWIN data for given pincode and write to a database'''
    # TODO: Current implementation will give slots for next week.
    # What about the dates in the future?
    pincode = Pincode.query.filter(Pincode.code==code).first()
    if pincode is None:
        print(f"Unknown pincode: {code}")
        return False

    data = cowin.findWeeklySessionsByPin(pincode.code)
    data_hashed = str(hash_calendar(data))
    if pincode.availabilities_hash != data_hashed:
        pincode.availabilities = data
        pincode.availabilities_hash = data_hashed
        db.session.commit()
        return True
    # No changes to calendar.
    return False

@celery.task
def updateSubscriber(subscription_id):
    '''Update the subscriber based on the new CoWIN data'''
    subscription = Subscription.query.filter(Subscription.id==subscription_id).first()
    if subscription is None:
        print(f"Unknown subscription: {subscription_id}")
        return False

    result = processNotifications(subscription)
    return result

@celery.task
def updateLog(part):
    message = f"Poller update: {part} at {datetime.datetime.now()}"
    print(message)
    return True

@celery.task
def updateAllPincodes():
    '''Fetch new data for all pincodes currently in the database.
    Returns a group so that this update can be executed in parallel'''
    callback = subtask(updatePincode.s())
    return group(callback.clone((pincode.code,)) for pincode in
        Pincode.query.filter(Pincode.subscriptions.any()).all())()

@celery.task
def updateAllSubscribers():
    '''Notify new data for all subscriptions currently in the database.
    Returns a group so that this update can be executed in parallel'''
    callback = subtask(updateSubscriber.s())
    return group(callback.clone((subscription.id,)) for subscription in
        Subscription.query.filter(Subscription.pincodes.any()).all())()

# Note: Groups chained together get upgraded to chords anyway
# This kind of "piping" syntax is more intuitive to read, so using it
all_tasks = (
    updateLog.si('beg') | 
    updateAllPincodes.si() | updateLog.si('mid') |
    updateAllSubscribers.si() | updateLog.si('end')
)

@celery.task
def periodicTask():
    return all_tasks()

celery.conf.beat_schedule = {
    'All shadja background updates': {
        'task': 'poller.periodicTask',
        'schedule': celery.conf.get('CELERY_BEAT_INTERVAL'),
        'args': ()
    }
}

if __name__=='__main__':
    pass
