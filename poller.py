'''
Script to be called by the cron job periodically to query CoWIN and update subscribers
'''

import consumer
import cowin

# FIXME: Temporary variable
all_data = {}

# Read the database to find which pincodes to query
def getAllPincodes():
    ''' Get a list of pincodes to query CoWIN'''
    # FIXME: Placeholder for now
    return [560090, 5600015]
    # TODO: Return an iterable here

def getAllConsumers():
    '''Get a list of consumers to process with new data'''
    # TODO: Connect a DB with ORM so that return value is a iterable of class instances
    # FIXME: Placeholder for now
    c = consumer.Consumer()
    c.pin_codes = [560090, 560015]
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

    # Find all valid slots in the pincodes
    available_slots - []
    # for pincode in consumer.pin_codes:
    #        data = all_data[pincode]
    #        if is_valid_session(data)

def queryCoWIN():
    '''Query CoWIN and update consumers of any relevant slots'''
    # Get data from CoWIN for each of these pincodes and update internal DB
    map(storeCoWINData, getAllPincodes())

    # Now, update the consumers if there are any relevant slots for them
    map(processNotifications, getAllConsumers())

if __name__=='__main__':
    queryCoWIN()
