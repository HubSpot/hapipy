from base import BaseClient
import logging_helper


CONTACT_LISTS_API_VERSION = '1'


class ContactListsClient(BaseClient):
    """
    The hapipy Contact Lists client uses the _make_request method to call the API for data.
    It returns a python object translated from the json return
    """

    def __init__(self, *args, **kwargs):
        super(ContactListsClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log('hapi.contact_lists')

    def _get_path(self, subpath):
        return 'contacts/v%s/%s' % (self.options.get('version') or CONTACT_LISTS_API_VERSION, subpath)

    def get_contact_lists(self, **options):
        return self._call('lists', method='GET', **options)

    def add_contact_to_a_list(self, list_id, data=None, **options):
        data = data or {}
        return self._call('lists/{list_id}/add'.format(list_id=list_id),
                          data=data, method='POST', **options)
