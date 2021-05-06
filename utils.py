'''Contains commmon utility functions'''

import hashlib
import os
import random

OtpMax = 9999 # 4 digit OTP
Salt = os.urandom(32)


def get_otp_hash():
    '''Generate a random 4 digit OTP and its corresponding hash'''
    otp = random.randint(0, OtpMax)
    return otp, get_hash(otp)

def get_hash(otp):
    '''Generate salted hmac hash'''
    key = hashlib.pbkdf2_hmac(
        'sha256', # The hash digest algorithm for HMAC
        str(otp).encode('utf-8'), # Convert the password to bytes
        Salt, # Provide the salt
        100000 # It is recommended to use at least 100,000 iterations of SHA-256 
    )
    return key
