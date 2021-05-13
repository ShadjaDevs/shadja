'''Contains different notification methods'''

import jinja2
import json
import os
import ElasticEmailClient as EmailClient
from shadja import app

# Global email settings for the notifications
EmailClient.ApiClient.apiKey = app.config.get("ELASTICEMAIL_KEY")
EmailApptSubject = 'We found new vaccine appointments for you'
EmailFrom = 'appointments@bookmyvaccine.app'
EmailFromName = 'BookMyVaccine'
EmailOTPSubject = 'OTP to verify your email'
UnsubscribeURL = 'https://api.bookmyvaccine.app/remove_subscription/{0}'

# return True if everything goes well
# so we can avoid sending this notification again
def notify_email(subscription, available_centers):
    '''Send an email using a bootstrap template with availability
    of slots'''
    bodyText = json.dumps(available_centers)
    bodyHtml = jinja2.Template(
        open('templates/email_slot_template.html').read()).render(
            available_centers=available_centers,
            unsub_url=UnsubscribeURL.format(subscription.uuid))
    to = subscription.email

    emailResponse = EmailClient.Email.Send(
        subject=EmailApptSubject,
        EEfrom=EmailFrom,
        fromName=EmailFromName,
        msgTo=[to],
        bodyText=bodyText,
        bodyHtml=bodyHtml,
        isTransactional=True,
        encodingType=EmailClient.ApiTypes.EncodingType.Base64)
    return True

# return True if everything goes well
# so we can avoid sending this notification again
def notify_mobile(subscription, available_centers):
    return False

# return True if everything goes well
# so we can avoid sending this notification again
def notify_telegram(subscription, available_centers):
    return False

# OTP methods
def send_otp_email(subscription, otp):
    '''Send an email using a bootstrap template with availability
    of slots'''

    bodyText = f'Your OTP to verify your email is {str(otp).zfill(4)}'
    bodyHtml = jinja2.Template(
        open('templates/email_otp_template.html').read()).render(
            otp=str(otp).zfill(4),
            unsub_url=UnsubscribeURL.format(subscription.uuid))
    to = subscription.email

    emailResponse = EmailClient.Email.Send(
        subject=EmailOTPSubject,
        EEfrom=EmailFrom,
        fromName=EmailFromName,
        msgTo=[to],
        bodyText=bodyText,
        bodyHtml=bodyHtml,
        isTransactional=True,
        encodingType=EmailClient.ApiTypes.EncodingType.Base64)
    return True

if __name__=='__main__':
    import models
    centers = {}
    subscription = models.Subscription(True)
    subscription.email = 'nikhil.soraba+bookmyvaccine@gmail.com'
    notify_email(subscription, centers)
    send_otp_email(subscription, 1234)
