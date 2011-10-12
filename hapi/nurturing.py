from base import BaseClient

NURTURING_API_VERSION = '1'

class NurturingClient(BaseClient):
  
    def _get_path(self, subpath):
        return 'nurture/v%s/%s' % (NURTURING_API_VERSION, subpath)
    
    def get_campaigns(self, **options):
        return self._call('campaigns', **options)
    
    def get_leads(self, campaign_guid, **options):
        return self._call('campaign/%s/list' % campaign_guid, **options)
    
    def get_history(self, lead_guid, **options):
        return self._call('lead/%s' % lead_guid, **options)
    
    def enroll_lead(self, campaign_guid, lead_guid, **options):
        return self._call('campaign/%s/add' % campaign_guid, data=lead_guid, method='POST', **options)
    
    def unenroll_lead(self, campaign_guid, lead_guid, **options):
        return self._call('campaign/%s/remove' % campaign_guid, data=lead_guid, method='POST', **options)
    

