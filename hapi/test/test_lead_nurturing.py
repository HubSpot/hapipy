import unittest2
import helper
from hapi import hapi
from pprint import pprint

class LeadNurtureTest(unittest2.TestCase):
    def setUp(self):
        creds = helper.get_creds()
        self.hapikey = creds.pop('hapikey')
        self.leftovers = creds
        self.controller = hapi.HubSpotLeadNurtureClient(self.hapikey, **self.leftovers)
    
    def tearDown(self):
        pass
        
    def test_get_campaigns(self):
        campaigns = self.controller.get_campaigns()
        [pprint(vars(c)) for c in campaigns]
        self.assertTrue(len(campaigns))

if __name__ == "__main__":
    unittest2.main()
