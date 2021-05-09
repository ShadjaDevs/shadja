'''
Module with python wrappers for CoWIN's public REST APIs
'''

import datetime
import requests
from fake_useragent import UserAgent

BaseURL = 'https://cdn-api.co-vin.in/api'
Version = 'v2'
AppointmentPath = 'appointment/sessions/public'
AppointmentEp = '/'.join([BaseURL, Version, AppointmentPath])

DateFormat = '%d-%m-%Y'
TimeFormat = '%I:%M%p'

def isValidPin(pincode):
    '''Check if supplied PIN is valid'''
    return isinstance(pincode, int) and (100000 <= pincode <= 999999)

def isValidDate(date):
    '''Check if supplied date is valid'''
    return isinstance(date, datetime.datetime)

def findDailySessionsByPin(pincode, date=None):
    ''' Takes a PIN and returns all the sessions for a given date from the CoWIN API'''

    # Get for the next 7 days from today by default
    if date is None:
        date = datetime.datetime.today()

    assert(isValidPin(pincode))
    assert(isValidDate(date))

    url = '/'.join([AppointmentEp, 'findByPin'])
    params = {
        'pincode': pincode,
        'date': date.strftime(DateFormat)
    }
    
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def findWeeklySessionsByPin(pincode, date=None):
    ''' Takes a PIN and returns all the sessions for a week starting from the given date from the CoWIN API'''

    # Get for the next 7 days from today by default
    if date is None:
        date = datetime.datetime.today()
 
    assert(isValidPin(pincode))
    assert(isValidDate(date))

    url = '/'.join([AppointmentEp, 'calendarByPin'])
    params = {
        'pincode': pincode,
        'date': date.strftime(DateFormat)
    }

    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__=='__main__':
    # print(findDailySessionsByPin(560090, datetime.datetime.today()))
    print(findWeeklySessionsByPin(560091))
