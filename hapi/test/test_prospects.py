import unittest2
import helper
import simplejson as json
from nose.plugins.attrib import attr
from hapi.prospects import ProspectsClient

class ProspectsClientTest(unittest2.TestCase):
    """ Unit tests for the HubSpot Prospects API Python client.

    This file contains some unittest tests for the Prospects API.

    It is not intended to be exhaustive, just simple exercises and
    illustrations, at this point.

    Additional tests and other improvements welcome.

    Questions, comments, etc: http://docs.hubapi.com/wiki/Discussion_Group
    """
    
    def setUp(self):
        self.client = ProspectsClient(**helper.get_options())
    
    def tearDown(self):
        pass
        
    @attr('api')
    def test_get_prospects(self):
        # List the prospects for our Hub ID.
        
        prospects = self.client.get_prospects()
        self.assertTrue(len(prospects))
        print "Got some prospects: %s" % json.dumps(prospects)
 
    @attr('api')
    def test_get_company(self):
        # Looks up a specific company.
        company = self.client.get_company('')

        # The company may or may not be a prospect.
        # self.assertTrue(len(company))
        print "Got the company timeline: %s" % json.dumps(company)

    @attr('api')
    def test_search_country(self):
        # Looks up prospects from a specific country.
        search_results = self.client.search_prospects('country', 'Czech')

        # There may or may not be recent prospects from this country.
        # self.assertTrue(len(search_results))
        print "Got some country search results: %s" % json.dumps(search_results)

    @attr('api')
    def test_search_region(self):
        # Looks up prospects from a specific region, e.g. US state.
        search_results = self.client.search_prospects('region', 'Massachusetts')

        # There may or may not be recent prospects from this region.
        # self.assertTrue(len(search_results))
        print "Got some region search results: %s" % json.dumps(search_results)

    @attr('api')
    def test_search_city(self):
        # Looks up prospects from a given city, e.g. Boston.
        search_results = self.client.search_prospects('city', 'Boston')

        # There may or may not be recent prospects from this city.
        # self.assertTrue(len(search_results))
        print "Got some city search results: %s" % json.dumps(search_results)

    @attr('api')
    def test_get_hidden_prospects(self):
        # Lists the prospects that have been "hidden" in this account, if any.
        hidden_prospects = self.client.get_hidden_prospects()
        
        # This account may or may not have hidden prospects.
        # self.assertTrue(len(hidden_prospects))
        print "Got %d hidden prospects: %s" % (len(hidden_prospects), json.dumps(hidden_prospects))

    @attr('api')
    def test_hide_prospect(self):
        # Tries to hide a prospect.
        data = self.client.hide_prospect('hubspot')

        # If there's no matching prospect, can't hide it, so this might return false.
        # self.assertTrue(len(response))
        print "Tried to hide a prospect: %s" % json.dumps(data)

    @attr('api')
    def test_unhide_prospect(self):
        # Tries to un-hide a hidden prospect.
        data = self.client.unhide_prospect('hubspot')

        # If there's no matching hidden prospect, can't un-hide it.
        # self.assertTrue(len(response))
        print "Tried to un-hide a prospect: %s" % json.dumps(data)
 
if __name__ == "__main__":
    unittest2.main()
