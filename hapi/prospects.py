from base import BaseClient

PROSPECTS_API_VERSION = 'v1'

class ProspectsClient(BaseClient):
  
    def _get_path(self, method):
        return 'prospects/%s/%s' % (PROSPECTS_API_VERSION, method)

    def get_prospects(self, offset=None, orgoffset=None):
        params = {}
        if offset:
          params['timeOffset'] = offset
          params['orgOffset'] = orgoffset
        return self._call('timeline', params)
        
    def get_company(self, company_slug):
        return self._call('timeline/%s' % company_slug)
        
    def search_prospects(self, search_type, query, offset=None, orgoffset=None):
        params = {'q': query}
        if offset and orgoffset:
          params['orgOffset'] = orgoffset
          params['timeOffset'] = offset
          
        return self._call('search/%s' % search_type, params)
        
    def get_hidden_prospects(self):
        return self._call('filters')
        
    def hide_prospect(self, company_name):
        return self._call('filters', data={'organization': company_name}, method="POST")
        
    def unhide_prospect(self, company_name):
        return self._call('filters', data={'organization': company_name}, method="DELETE")
        
    def get_options_for_query(self, query):
        return self._call('typeahead/', {'q': query})
