from hapi_plus.base import BaseClient

GROUPS_API_VERSION = '1'


class GroupsClient(BaseClient):

    def _get_path(self, subpath):
        return 'contacts/v%s/%s' % (GROUPS_API_VERSION, subpath)

    def get_groups(self, **options):
        return self._call('groups', **options)

    def get_group(self, group_name, **options):
        return self._call('groups/%s' % group_name, **options)

    def create_group(self, group_name,data, **options):
        return self._call('groups/%s' % group_name, data=data, method='PUT', **options)

    def update_group(self, group_name, data, **options):
        return self._call('groups/%s' % group_name, data=data, method='POST', **options)

    def delete_group(self, group_name, **options):
        return self._call('groups/%s' % group_name, method='DELETE', **options)
