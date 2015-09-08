from base import BaseClient
import logging_helper


CONTACTS_API_VERSION = '1'


class ContactsClient(BaseClient):
    """
    The hapipy Contacts client uses the _make_request method to call the API for data.
    It returns a python object translated from the json return
    """

    def __init__(self, *args, **kwargs):
        super(ContactsClient, self).__init__(*args, **kwargs)
        self.log = logging_helper.get_log('hapi.contacts')

    def _get_path(self, subpath):
        return 'contacts/v%s/%s' % (self.options.get('version') or CONTACTS_API_VERSION, subpath)

    def create_or_update_a_contact(self, email, data=None, **options):
        data = data or {}
        return self._call('contact/createOrUpdate/email/{}'.format(email),
                          data=data, method='POST', **options)
