from base import BaseClient

EVENTS_API_VERSION = 1

class EventsClient(BaseClient):
  
    def get_path(self, subpath):
        return 'events/v%s/%s' % (EVENTS_API_VERSION, subpath)
    
    def get_events(self, **options):
        return self.call('events', **options)
    
    def create_event(self, description, create_date, url, event_type, **options):
        event_data = {
            'description': description,
            'createDate': create_date,
            'url': url,
            'eventType': event_type
        }
        return self.call('events', data=event_data, method='POST', **options)

