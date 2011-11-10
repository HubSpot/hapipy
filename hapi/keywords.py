from base import BaseClient

KEYWORDS_API_VERSION = '1'

class KeywordsClient(BaseClient):
    
    def _get_path(self, subpath):
        return 'keywords/v%s/%s' % (KEYWORDS_API_VERSION, subpath)
    
    def get_keywords(self, **options):
        return self._call('keywords', **options)['keywords']
    
    def get_keyword(self, keyword_guid, **options):
        return self._call('keywords/%s' % keyword_guid, **options)
    
    def add_keyword(self, keyword, **options):
        return self._call('keywords', data=dict(keyword=str(keyword)), method='PUT', **options)
    
    def add_keywords(self, keywords, **options):
        data = []
        for keyword in keywords:
            if keyword != '':
                data.append(dict(keyword=str(keyword)))
        return self._call('keywords', data=data, method='PUT', **options)['keywords']
    
    def delete_keyword(self, keyword_guid, **options):
        return self._call('keywords/%s' % keyword_guid, method='DELETE', **options)
