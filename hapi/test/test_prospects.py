import unittest2
import helper
import simplejson as json
from nose.plugins.attrib import attr
from hapi.prospects import ProspectsClient
 
class ProspectsClientTest(unittest2.TestCase):
    def setUp(self):
        self.client = ProspectsClient(**helper.get_options())
    
    def tearDown(self):
        pass
        
    @attr('api')
    def test_get_prospects(self):
        prospects = self.client.get_prospects()
        self.assertTrue(len(prospects))
        print "Got some prospects: %s" % json.dumps(prospects)
 
    @attr('api')
    def test_get_company(self):
        company = self.client.get_company('')
        self.assertTrue(len(company))
        print "Got the company timeline: %s" % json.dumps(company)

    @attr('api')
    def test_search_country(self):
        search_results = self.client.search_prospects('country', 'Czech')
        self.assertTrue(len(search_results))
        print "Got some country search results: %s" % json.dumps(search_results)

    @attr('api')
    def test_search_region(self):
        search_results = self.client.search_prospects('region', 'Massachusetts')
        self.assertTrue(len(search_results))
        print "Got some region search results: %s" % json.dumps(search_results)

    @attr('api')
    def test_search_city(self):
        search_results = self.client.search_prospects('city', 'Boston')
        self.assertTrue(len(search_results))
        print "Got some city search results: %s" % json.dumps(search_results)

    @attr('api')
    def test_get_hidden_prospects(self):
        hidden_prospects = self.client.get_hidden_prospects()
        # Can't assert, as this portal may have 0 or many hidden prospects.
        # self.assertTrue(len(hidden_prospects))
        print "Got %d hidden prospects: %s" % (len(hidden_prospects), json.dumps(hidden_prospects))

    @attr('api')
    def test_hide_prospect(self):
        data = self.client.hide_prospect('HubSpot')
        # If there's no matching prospect, can't hide it, so this might return false.
        # self.assertTrue(len(response))
        print "Tried to hide a prospect: %s" % json.dumps(data)

    @attr('api')
    def test_unhide_prospect(self):
        data = self.client.unhide_prospect('HubSpot')
        # If there's no matching hidden prospect, can't un-hide it.
        # self.assertTrue(len(response))
        print "Tried to un-hide a prospect: %s" % json.dumps(data)
 
if __name__ == "__main__":
    unittest2.main()
