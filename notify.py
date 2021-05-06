'''Contains different notification methods'''

from ElasticEmailClient import ApiClient, Email

def notify_email(consumer, available_centers):
    '''Send an email using a bootstrap template with availability
    of slots'''
    print(f"emailing {consumer} with {available_centers}")
    pass

# TODO: Elastic mail API: need to work on it after domain is registered
# ApiClient.apiKey = '11111111-2222-3333-4444-555555555555'

# subject = 'Your subject'
# fromEmail = 'Your Email'
# fromName = 'Your Company Name'
# bodyText = 'Text body'
# bodyHtml = '<h1>Hello, {username}.</h1>'
# files = { 'C:/Users/recipients.csv' }
# filenameWithRecipients = 'recipients.csv' # same as the file above

# emailResponse = Email.Send(subject, fromEmail, fromName, bodyText = bodyText, bodyHtml = bodyHtml, attachmentFiles = files, mergeSourceFilename = filenameWithRecipients)


# try:
#     print ('MsgID to store locally: ', emailResponse['messageid'], end='\n') # Available only if sent to a single recipient
#     print ('TransactionID to store locally: ', emailResponse['transactionid'])
# except TypeError:
#     print ('Server returned an error: ', emailResponse)

def notify_mobile(consumer, available_centers):
    pass

def notify_telegram(consumer, available_centers):
    pass
