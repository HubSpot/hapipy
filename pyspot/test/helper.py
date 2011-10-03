import os
import json


def get_creds():
    filename = 'test_credentials.json'
    try:
        raw_text = open(os.path.join(os.path.dirname(__file__), filename)).read()
    except IOError:
        raise Exception, """
            Unable to open '%s' for integration tests.\n
            These tests rely on the existence of that file and on it having valid hubspo api credentials.""" % filename
    try:
        creds = json.loads(raw_text)
    except ValueError:
        raise Exception, """
            '%s' doesn't appear to be valid json!\n
            These tests rely on the existence of that file and on it having valid hubspot api credentials.""" % filename

    if not creds.get('hapikey'):
        raise Exception, """
            '%s' seems to have no 'hapikey' specified!\n
            These tests rely on the existence of that file and on it having valid hubspot api credentials.""" % filename

    return creds
    

