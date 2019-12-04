from .base import BaseClient
from . import logging_helper
from future.moves.urllib.parse import quote


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
        """ Creates or Updates a client with the supplied data. """
        data = data or {}
        return self._call('contact/createOrUpdate/email/{email}'.
                          format(email=quote(email.encode('utf-8'))),
                          data=data, method='POST', **options)

    def get_contact_by_email(self, email, **options):
        """ Gets contact specified by email address. """
        return self._call('contact/email/{email}/profile'.
                          format(email=quote(email.encode('utf-8'))),
                          method='GET', **options)

    def update_a_contact(self, contact_id, data=None, **options):
        """ Updates the contact by contact_id with the given data. """
        data = data or {}
        return self._call('contact/vid/{contact_id}/profile'.format(contact_id=contact_id),
                          data=data, method='POST', **options)

    def delete_a_contact(self, contact_id, **options):
        """ Deletes a contact by contact_id. """
        return self._call('contact/vid/{contact_id}'.
                          format(contact_id=contact_id), method='DELETE', **options)
