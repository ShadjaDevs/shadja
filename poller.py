'''
Script to be called by the cron job periodically to query CoWIN and update subscribers
'''

import datetime

import consumer
import cowin
import notify

# FIXME: Temporary variable
all_data = {}

# Read the database to find which pincodes to query
def getAllPincodes():
    ''' Get a list of pincodes to query CoWIN'''
    # FIXME: Placeholder for now
    return [560090, 560015]
    # TODO: Return an iterable here

def getAllConsumers():
    '''Get a list of consumers to process with new data'''
    # TODO: Connect a DB with ORM so that return value is a iterable of class instances
    # FIXME: Placeholder for now
    c = consumer.Consumer()
    c.pincodes = [560090, 560015]
    c.old = True
    c.to_email = True
    return [c]

def storeCoWINData(pincode):
    '''Get CoWIN data for given pincode and write to a database'''
    # TODO: Current implementation will give slots for next week. What about the dates in the future?
    data = cowin.findWeeklySessionsByPin(pincode)
    # FIXME: Placeholder for now
    global all_data
    all_data[pincode] = data

def processNotifications(consumer):
    '''Notify the consumers if there are new slots opening up'''
    global all_data

    # Define functions for this consumer
    def is_valid_center(center):
        # TODO: Check that the keys exist
        # Do not assume
        valid = \
            (center['pincode'] in consumer.pincodes) and \
            ((consumer.want_free is None) or \
                (consumer.want_free == (center['fee_type']=='Free')))
        return valid

    def is_valid_session(session):
        session['date'] = datetime.datetime.strptime(session['date'], cowin.DateFormat)
        
        valid = ((consumer.date_start is None) and \
                (consumer.date_end is None)) or \
            (consumer.date_start <= session['date'] <= consumer.date_end) and \
            (session['available_capacity'] > 0) and \
            ((consumer.flavor is None) or (consumer.flavor==center['vaccine'].lower())) and \
            (consumer.old or (center['min_age_limit']==18))
        return valid

    def is_valid_slot(slot):
        start_time, _, end_time = slot.partition('-')

        start_time = datetime.datetime.strptime(start_time, cowin.TimeFormat)
        end_time   = datetime.datetime.strptime(end_time, cowin.TimeFormat)

        # Need to find out if this slot has any overlap with the slot user is requesting
        # Interestingly, this is not trivial
        # https://stackoverflow.com/questions/3269434/whats-the-most-efficient-way-to-test-two-integer-ranges-for-overlap
        valid = ((consumer.time_start is None) and \
                (consumer.time_end is None)) or \
            ((consumer.time_start <= end_time) and \
             (consumer.time_end   >= start_time))
        return valid

    # Find all valid slots in the pincodes
    available_centers = {}

    for pincode in consumer.pincodes:
        # FIXME: This should be a DB read
        data = all_data[pincode]

        # At this moment, assuming no guarantees
        # about this JSON data. Hence, checking
        # for the key in JSON before trying to access it.
        # Look before you leap approach
        if 'centers' not in data:
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
            center['sessions'] = list(filter(lambda session: len(session['slots'])>0, sessions))

        # Filter out centers with no valid sessions
        available_centers[pincode] = list(filter(lambda center: len(center['sessions'])>0, centers))

    # Send the notification
    # TODO: If previously informed of the same, should you still do? May be yes
    if consumer.email:
        notify.notify_email(consumer, available_centers)

    # if consumer.mobile:
    #     notify_mobile(consumer, available_centers)

    # if consumer.telegram_id:
    #     notify_mobile(consumer, available_centers)

def queryCoWIN():
    '''Query CoWIN and update consumers of any relevant slots'''
    # Get data from CoWIN for each of these pincodes and update internal DB
    for pincode in getAllPincodes():
        storeCoWINData(pincode)

    # Now, update the consumers if there are any relevant slots for them
    for consumer in getAllConsumers():
        processNotifications(consumer)

if __name__=='__main__':
    queryCoWIN()
