from hapi_plus.base import BaseClient
import unicodedata
import re

GROUPS_API_VERSION = '1'


class GroupsClient(BaseClient):

    def _get_path(self, subpath):
        return 'contacts/v%s/%s' % (GROUPS_API_VERSION, subpath)

    def get_groups(self, **options):
        return self._call('groups', **options)

    def get_group(self, group_name, **options):
        valid_name = validate_name(group_name)
        return self._call('groups/%s' % valid_name, **options)

    def create_group(self, group_name,data, **options):
        valid_name = validate_name(group_name)
        return self._call('groups/%s' % valid_name, data=data, method='PUT', **options)

    def update_group(self, group_name, data, **options):
        valid_name = validate_name(group_name)
        return self._call('groups/%s' % valid_name, data=data, method='POST', **options)

    def delete_group(self, group_name, **options):
        valid_name = validate_name(group_name)
        return self._call('groups/%s' % valid_name, method='DELETE', **options)

    def validate_group_name(self, group_name):
        slug = unicodedata.normalize('NFKD', group_name)
        slug = slug.encode('ascii', 'ignore').lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
        slug = re.sub(r'[-]+', '-', slug)
        
        return slug
