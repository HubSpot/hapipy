from hapi_plus.base import BaseClient

PROPERTIES_API_VERSION = '1'


class PropertiesClient(BaseClient):

    def _get_path(self, subpath):
        return 'contacts/v%s/%s' % (PROPERTIES_API_VERSION, subpath)

    def get_property(self, property_name, **options):
        return self._call('properties/%s' % property_name, **options)

    def get_properties(self, **options):
        return self._call('properties', **options)

    def get_grouped_properties(self, **options):
        return self._call('properties', {'grouped': True}, **options)

    def create_property(self, property_name, data, **options):
        return self._call('properties/%s' % property_name, data=data, method='PUT', **options)

    def update_property(self, property_name, data, **options):
        return self._call('properties/%s' % property_name, data=data, method='POST', **options)

    def delete_property(self, property_name, **options):
        return self._call('properties/%s' % property_name, method='DELETE', **options)