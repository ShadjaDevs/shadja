'''
Contains consumer class
'''

class Consumer:
    '''Class object to represent every new _request_ added to the system by users'''
    def __init__(self):
        # List of interested pincodes
        self.pincodes = [] # list of numbers

        # Assume under 45 by default
        self.old = False # Boolean

        # By default, free or paid are ok
        self.want_free = None # Boolean/None

        # By default, any flavor is ok
        # UI to make sure flavor is not left blank when
        # only second shot is requested
        self.flavor = None # String

        # Optional date and time range (instances of datetime.datetime class)
        self.date_start = None
        self.date_end = None
        self.time_start = None
        self.time_end = None

        # Info for notification
        self.email = None
        self.mobile = None
        self.telegram_id = None

        # Notifications requested flags
        self.to_email = False # Boolean
        self.to_mobile = False # Boolean
        self.to_telegram = False # Boolean

if __name__=='__main__':
    c = Consumer()