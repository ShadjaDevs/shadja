'''
Module with python wrappers for CoWIN's public REST APIs
'''

import datetime
import requests
import utils
from fake_useragent import UserAgent

BaseURL = 'https://cdn-api.co-vin.in/api'
Version = 'v2'
AppointmentPath = 'appointment/sessions/public'
AppointmentEp = '/'.join([BaseURL, Version, AppointmentPath])
PERIOD_TO_API_STRING = {
    "day": "findBy",
    "week": "CalendarBy"
}

def isValidPin(pincode):
    '''Check if supplied PIN is valid'''
    return isinstance(pincode, int) and (100000 <= pincode <= 999999)

def isValidDate(date):
    '''Check if supplied date is valid'''
    return isinstance(date, datetime.datetime)

def findAppointments(jurisdiction, period, region_id, date=None):
    """
    Find appointments by region_id, for a jurisdiction, for 1 or 7 days.

    Args:

    jurisdiction
      string - either "district", "pin"
    period
      string - either "day", "week"
    region_id
      string - pincode or district id
    date
      date - in utils.DateFormat

    Returns:

    response json from API as documented in https://apisetu.gov.in/public/api/cowin#/

    Raises:

      AssertionError
      request.raise_for_status()
    """
    jurisdiction = jurisdiction.lower().title() 
    period = period.lower()
    # Get for the next 7 days from today by default
    if date is None:
        date = datetime.datetime.today()

    assert(jurisdiction in ["District", "Pin"])
    assert(period in ["day", "week"])
    assert(isValidPin(region_id))
    assert(isValidDate(date))

    api = PERIOD_TO_API_STRING[period]+jurisdiction

    url = '/'.join([AppointmentEp, api])
    params = {
        'region_id': region_id,
        'date': date.strftime(utils.DateFormat)
    }
    
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def findDailySessionsByPin(pincode, date=None):
    ''' Takes a PIN and returns all the sessions for a given date from the CoWIN API'''
    return findAppointments("pin", "day", pincode, date)


def findWeeklySessionsByPin(pincode, date=None):
    ''' Takes a PIN and returns all the sessions for a week starting from the given date from the CoWIN API'''
    return findAppointments("pin", "week", pincode, date)

def findWeeklySessionsByDistrict(district, date=None):
    return findAppointments("district", "week", district, date)

if __name__=='__main__':
    # print(findDailySessionsByPin(560090, datetime.datetime.today()))
    print(findWeeklySessionsByPin(560091))
