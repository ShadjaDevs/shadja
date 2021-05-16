'''Contains commmon utility functions'''

import datetime
import hashlib
import os
import random
import uuid

import pyisemail

OtpMax = 9999 # 4 digit OTP
DateFormat = '%d-%m-%Y'
TimeFormat = '%I:%M%p'

# These are the radii present in the mongoDB (precomputed)
ValidRadii = [5, 10, 25, 50]
# Current vaccine flavors available in India
ValidFlavors = ['covishield', 'covaxin']

#TODO: Make salt random and store it
Salt = os.environ['SHADJA_SETTINGS']


def get_otp_hash():
    '''Generate a random 4 digit OTP and its corresponding hash'''
    otp = random.randint(0, OtpMax)
    return otp, get_hash(otp)

def get_hash(otp):
    '''Generate salted hmac hash'''
    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        str(otp).encode('utf-8'), # Convert the password to bytes
        Salt.encode('utf-8'), # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    return key.hex()

def isValidPin(pincode):
    '''Check if supplied PIN is valid'''
    return isinstance(pincode, int) and (100000 <= pincode <= 999999)

def isValidFlavor(flavor):
    '''Check if supplied flavor is valid'''
    return isinstance(flavor, str) and (flavor in ValidFlavors)


def isValidDate(date):
    '''Check if supplied date is valid'''
    return isinstance(date, datetime.datetime)

def isValidDateStr(date):
    '''Check if supplied date string is valid'''
    try:
        if date != datetime.datetime.strptime(date, DateFormat).strftime(DateFormat):
            raise ValueError
        return True
    except ValueError:
        return False

def isValidEmail(email):
    '''Check if supplied email is valid'''
    return isinstance(email, str) and pyisemail.is_email(email)

def isValidMobile(mobile):
    '''Check if supplied mobile is valid'''
    return isinstance(mobile, int) and (1000000000 <= mobile <= 9999999999)

def isValidTelegramId(telegram_id):
    '''Check if supplied telegram id is valid'''
    return True

def isValidRadius(radius):
    '''Check if supplied radius is valid'''
    return isinstance(radius, int) and (radius in ValidRadii)

def isValidOTP(otp):
    '''Check if supplied OTP is in valid format'''
    return isinstance(otp, int) and (0 <= otp <= OtpMax)

def isValidUUID(uid):
    '''
    https://gist.github.com/ShawnMilo/7777304
    Validate that a UUID string is in
    fact a valid uuid4.
    Happily, the uuid module does the actual
    checking for us.
    It is vital that the "version" kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.
    '''
    try:
        val = uuid.UUID(uid, version=4)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False

    # If the uid is a valid hex code, 
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a 
    # valid uuid4. This is bad for validation purposes.

    return str(val).lower() == str(uid).lower()

def getDateFromDateStr(date):
    '''Return date in datetime.date object'''
    return datetime.datetime.strptime(date, DateFormat).date()
