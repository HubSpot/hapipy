import random
import unittest2

import simplejson as json
from nose.plugins.attrib import attr

import helper
from hapi.events import EventsClient

class EventsClientTest(unittest2.TestCase):
    """ Unit tests for the HubSpot Events API Python client.

    This file contains some unittest tests for the Events API.

    Docs: http://docs.hubapi.com/wiki/Events_API

    Questions, comments: http://docs.hubapi.com/wiki/Discussion_Group
    """

    def setUp(self):
        self.client = EventsClient(**helper.get_options())
    
    def tearDown(self):
        pass
    
    @attr('api')
    def test_get_events(self):
        # Get all events, a lengthy list typically.
        events = self.client.get_events()
        self.assertTrue(len(events))
        
        print "\n\nGot some events: %s" % json.dumps(events)

    @attr('api')
    def test_create_events(self):        
        # Creates a test event.
        # Passing None for creation date/time means right-now on the API server.
        result = self.client.create_event("Test description", None, 'https://github.com/HubSpot/hapipy/', 'hapipy test')
        # This is just a 201 response (or 500), no contents.
         
        print "\n\nCreated event."

if __name__ == "__main__":
    unittest2.main()
