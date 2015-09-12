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
        """ Returns all of the contact lists """
        return self._call('lists', method='GET', **options)

    def add_contact_to_a_list(self, list_id, vids, data=None, **options):
        """ Adds a list of contact vids to the specified list. """
        data = data or {}
        data['vids'] = vids
        return self._call('lists/{list_id}/add'.format(list_id=list_id),
                          data=data, method='POST', **options)

    def create_a_contact_list(self, list_name, portal_id, dynamic=True, data=None, **options):
        """ Creates a contact list with given list_name on the given portal_id. """
        data = data or {}
        data['name'] = list_name
        data['portal_id'] = portal_id
        data['dynamic'] = dynamic
        return self._call('lists', data=data, method='POST', **options)

    def delete_a_contact_list(self, list_id, **options):
        """ Deletes the contact list by list_id. """
        return self._call('lists/{list_id}'.format(list_id=list_id), method='DELETE', **options)
