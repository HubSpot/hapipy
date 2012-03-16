import httplib
import logging
from error import HapiError


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
    

def get_log(name):
    logger = logging.getLogger(name)
    logger.addHandler(NullHandler())
    return logger


def auth_checker(access_token):
    # Do a simple api request using the access token
    connection = httplib.HTTPSConnection('api.hubapi.com')
    connection.request('GET', '/events/v1/events?max=1&access_token=%s' % access_token)
    result = connection.getresponse()
    return result.status


def refresh_access_token(refresh_token, client_id):
    # Refreshes an OAuth access token
    payload = 'refresh_token=%s&client_id=%s&grant_type=refresh_token' % (refresh_token, client_id)
    connection = httplib.HTTPSConnection('api.hubapi.com')
    connection.request('POST', '/auth/v1/refresh', payload)
    result = connection.getresponse()
    return result.read()

