import unittest2
import helper
from hapi.leads import LeadsClient
import logger
import time

class LeadsClientTest(unittest2.TestCase):
    def setUp(self):
        self.client = LeadsClient(**helper.get_options())
    
    def tearDown(self):
        pass

    def test_camelcased_params(self):
        in_options = { 
                'sort': 'fce.convert_date', 
                'search': 'BlahBlah', 
                'time_pivot': 'last_modified_at', 
                'is_not_imported': True }
        out_options = { 
                'sort': 'fce.convertDate', 
                'search': 'BlahBlah', 
                'timePivot': 'lastModifiedAt', 
                'isNotImported': 'true' }
        self.assertEquals(out_options, self.client.camelcase_search_options(in_options))
 

if __name__ == "__main__":
    unittest2.main()
