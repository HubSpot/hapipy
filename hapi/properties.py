from hapi_plus.base import BaseClient
import unicodedata
import re

PROPERTIES_API_VERSION = '1'


class PropertiesClient(BaseClient):

    def _get_path(self, subpath):
        return 'contacts/v%s/%s' % (PROPERTIES_API_VERSION, subpath)

    def get_property(self, property_name, **options):
        valid_name = validate_name(property_name)
        return self._call('properties/%s' % valid_name, **options)

    def get_properties(self, **options):
        return self._call('properties', **options)

    def get_grouped_properties(self, **options):
        return self._call('properties', {'grouped': True}, **options)

    def create_property(self, property_name, data, **options):
        valid_name = validate_name(property_name)
        return self._call('properties/%s' % valid_name, data=data, method='PUT', **options)

    def update_property(self, property_name, data, **options):
        valid_name = validate_name(property_name)
        return self._call('properties/%s' % valid_name, data=data, method='POST', **options)

    def delete_property(self, property_name, **options):
        valid_name = validate_property_name)
        return self._call('properties/%s' % valid_name, method='DELETE', **options)
        
    def validate_property_name(self, name):
        slug = unicodedata.normalize('NFKD', s)
        slug = slug.encode('ascii', 'ignore').lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
        slug = re.sub(r'[-]+', '-', slug)
        
        return slug
