from base import BaseClient

SETTINGS_API_VERSION = '1'

class SettingsClient(BaseClient):
    
    def get_path(self, subpath):
        return 'settings/v%s/%s' % (SETTINGS_API_VERSION, subpath)
    
    def get_settings(self, **options):
        return self.call('settings', **options)
    
    def update_settings(self, data, **options):
        return self.call('settings', data=data, method='POST', **options)
  

