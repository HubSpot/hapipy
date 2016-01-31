from hapi_plus.base import BaseClient

CONTACTS_API_VERSION = '1'


class ListsClient(BaseClient):

    def _get_path(self, subpath):
        return 'contacts/v%s/%s' % (CONTACTS_API_VERSION, subpath)

    def get_list(self, list_id, **options):
        return self._call('lists/%s' % list_id, **options)

    def get_batch_lists(self, list_ids, **options):
        return self._call('lists/batch', doseq=True, params={'listId': list_ids}, **options)

    def get_lists(self, count=20, offset=0, **options):
        return self._call('lists', {'count': count, 'offset': offset}, **options)

    def get_all_lists(self):
        count = 100
        has_more = True
        offset = 0
        lists = []

        while has_more:
            response = self.get_lists(count=count, offset=offset)
            lists.extend(response.get('lists', []))

            has_more = response.get('has-more')
            offset += response.get('offset')

        return lists

    def get_static_lists(self, count=20, offset=0, **options):
        return self._call('lists/static', {'count': count, 'offset': offset}, **options)

    def get_dynamic_lists(self, count=20, offset=0, **options):
        return self._call('lists/dynamic', {'count': count, 'offset': offset}, **options)

    def get_list_contacts(self, list_id, offset=None, properties=None, count=20, **options):
        params = {}

        if offset:
            params['vidOffset'] = offset

        if properties:
            params['property'] = properties

        if count:
            params['count'] = count

        return self._call('lists/%s/contacts/all' % list_id, params, doseq=True, **options)

    def get_list_contacts_recent(self, list_id, offset=None, properties=None, **options):
        params = {}

        if offset:
            params['timeOffset'] = offset

        if properties:
            params['property'] = properties

        return self._call('lists/%s/contacts/recent' % list_id, params, doseq=True, **options)

    def create_list(self, data, **options):
        return self._call('lists/', data=data, method='POST', **options)

    def update_list(self, list_id, data, **options):
        return self._call('lists/%s' % list_id, data=data, method='POST', **options)

    def add_contacts_to_list_from_emails(self, list_id, emails, **options):
        data = {'emails': emails}
        return self._call('lists/%s/add' % list_id, doseq=True, data=data, method='POST', **options)

    def add_contact_to_list(self, list_id, contact_id, doseq=True, **options):
        data = {'vids': [int(contact_id)]}
        return self._call('lists/%s/add' % list_id, data=data, doseq=True, method='POST', **options)

    def remove_contact_from_list(self, list_id, contact_id, doseq=True, **options):
        data = {'vids': [int(contact_id)]}
        return self._call('lists/%s/remove' % list_id, data=data, method='POST', **options)

    def delete_list(self, list_id, **options):
        return self._call('lists/%s' % list_id, method='DELETE', **options)

    def refresh_list(self, list_id, **options):
        return self._call('lists/%s/refresh' % list_id, method='POST', **options)

    def get_list_intersection(self, include_ids, exclude_ids):
        return self._call('lists/intersection/start', doseq=True, params={'include': include_ids, 'exclude': exclude_ids})

    def get_list_intersection_status(self, guid):
        return self._call('lists/intersection/%s/status' % (guid,))
