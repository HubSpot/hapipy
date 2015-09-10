import unittest2
import random

from nose.plugins.attrib import attr

import helper
from hapi.contact_lists import ContactListsClient
from hapi.contacts import ContactsClient
from test_contacts import ContactsClientTestCase


class ConstactListsClientTestCase(unittest2.TestCase):
    
    """ Unit tests for the HubSpot Contact Lists API Python client.

    This file contains some unittest tests for the Contact Lists API.

    Questions, comments: http://developers.hubspot.com/docs/methods/lists/create_list
    """

    test_portal_id = 62515

    def setUp(self):
    	self.client = ContactListsClient(**helper.get_options())
    	self.contacts_client = ContactsClient(**helper.get_options())
    	self.lists = []
    	self.contacts =[]

    def tearDown(self):
    	""" Clean up all the created objects. """
    	if self.contacts:
    		[self.contacts_client.delete_a_contact(contact) for contact in self.contacts]
    	if self.lists:
    		[self.client.delete_a_contact_list(list) for list in self.lists]

    @attr('api')
    def test_get_a_contact_lists(self):
    	""" Test that the get contact lists endpoint is valid. """
    	response = self.client.get_a_contact_lists()
    	self.assertTrue(len(response) > 0)

    @attr('api')
    def test_add_contact_to_a_list(self):
    	""" Test that the add contact to a list endpoint is valid. """
    	email = ContactsClientTestCase.test_contact_json['properties'][0]['value']
    	contact = self.contacts_client.create_or_update_a_contact(email, data=ContactsClientTestCase.test_contact_json)['vid']
    	self.contacts.append(contact)
    	contact_list = self.client.create_a_contact_list(list_name='test_add_contact_to_a_list' + str(random.randint(1000, 50000)),
    												   portal_id=self.test_portal_id,
    												   dynamic=False)
    	self.lists.append(contact_list['listId'])

    	response = self.client.add_contact_to_a_list(contact_list['listId'], [contact])
    	self.assertTrue(len(response) > 0)

    def test_create_a_contact_list(self):
    	""" Test that the create contact list endpoint is valid. """
    	response = self.client.create_a_contact_list(list_name='test_create_a_contact_list' + str(random.randint(1000, 50000)),
    											   portal_id=self.test_portal_id,
    											   dynamic=False)
    	self.assertTrue(len(response) > 0)

    	self.lists.append(response['listId'])

    def test_delete_a_contact_list(self):
    	""" Test that the delete contact list endpoint is valid. """
    	contact_list = self.client.create_a_contact_list(list_name='test_delete_a_contact_list' + str(random.randint(1000, 50000)),
    												   portal_id=self.test_portal_id,
    												   dynamic=False)

    	response = self.client.delete_a_contact_list(contact_list['listId'])
    	