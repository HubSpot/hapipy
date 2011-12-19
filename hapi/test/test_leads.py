import unittest2
import helper
from hapi.leads import LeadsClient
import logger
import time
import socket

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

    def test_get_leads(self):
        self.assertEquals(2, len(self.client.get_leads(max=2)))
        
    def test_open_lead(self):
        lead_guid = self.client.get_leads(timePivot='closedAt', startTime=0, max=1)[0]['guid']
        self.client.open_lead(lead_guid)
        time.sleep(3)
        self.assertEquals(False, self.client.get_lead(lead_guid)['isCustomer']) 

    def test_close_lead(self):
        # try to find a closed lead to open since we cannot explicitly search for open leads.
        try:
            lead_guid = self.client.get_leads(timePivot='closedAt', startTime=0, max=1)[0]['guid']
        except IndexError: # there were no closed leads, so we can just grab the first lead and trust that it is open.
            lead_guid = self.client.get_leads(max=1)[0]['guid']
            try:
                self.client.close_lead(lead_guid)
            except socket.timeout:
                raise Exception("[ERROR] close_lead timed out.")
            except Exception as e:
                raise Exception("[ERROR] Something went wrong closing the lead.")
            time.sleep(3)
            # make sure lead_guid is now a customer.
            self.assertEquals(True, self.client.get_lead(lead_guid)['isCustomer'])
            return
        # okay, we found a closed lead. Let's open it so we can close it again.
        try:
            self.client.open_lead(lead_guid)
        except socket.timeout:
            raise Exception("[ERROR] open_lead timed out.")
        except Exception as e:
            raise Exception("[ERROR] Something went wrong opening the lead.")
        # let's close this lead!
        try:
            self.client.close_lead(lead_guid)
        except socket.timeout:
            raise Exception("[ERROR] close_lead timed out.")
        except Exception as e:
            raise Exception("[ERROR] Something went wrong closing the lead.")
        # let's give HubSpotProcessing a few seconds in case it is busy
        time.sleep(3)
        # make sure close_lead worked.
        self.assertEquals(True, self.client.get_lead(lead_guid)['isCustomer'])

if __name__ == "__main__":
    unittest2.main()
