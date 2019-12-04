import os
import json
from . import logger


def get_options():
    filename = 'test_credentials.json'
    path = os.path.join(os.path.dirname(__file__), filename)
    options = {'api_key':'demo'}
    #options = {'access_token':'your_access_token', 'refresh_token':'clients_refresh_token', 'client_id':'your_app_client_ID'}
    if os.path.exists(path):
        try:
            raw_text = open(path).read()
        except IOError:
            raise Exception("""
                Unable to open '%s' for integration tests.\n
                If this file exists, then you are indicating you want to override the standard 'demo' creds with your own.\n
                However, it is currently inaccessible so that is a problem.""" % filename)
        try:
            options = json.loads(raw_text)
        except ValueError:
            raise Exception("""
                '%s' doesn't appear to be valid json!\n
                If this file exists, then you are indicating you want to override the standard 'demo' creds with your own.\n
                However, if I can't understand the json inside of it, then that is a problem.""" % filename)

        if not options.get('api_key') and not options.get('hapikey'):
            raise Exception("""
                '%s' seems to have no 'api_key' or 'access_token' specified!\n
                If this file exists, then you are indicating you want to override the standard 'demo' creds with your own.\n
                However, I'll need at least an API key to work with, or it definitely won't work.""" % filename)
        options['api_key'] = options.get('api_key') or options.get('hapikey')

    return options
    

