'''Contains different notification methods'''

def notify_email(consumer, available_centers):
    '''Send an email using a bootstrap template with availability
    of slots'''
    print(f"emailing {consumer} with {available_centers}")

def notify_mobile(consumer, available_centers):
    pass

def notify_telegram(consumer, available_centers):
    pass
