import unittest2

from faker import Faker
from nose.plugins.attrib import attr

import helper
from hapi.contacts import ContactsClient

fake = Faker()

class ContactsClientTestCase(unittest2.TestCase):
    
    """ Unit tests for the HubSpot Contacts API Python client.

    This file contains some unittest tests for the Contacts API.

    Questions, comments: http://developers.hubspot.com/docs/methods/contacts/contacts-overview
    """

    test_contact_json = {
            "properties": [
                {
                    "property": "email",
                    "value": fake.email()
                },
                {
                    "property": "firstname",
                    "value": fake.first_name()
                },
                {
                    "property": "lastname",
                    "value": fake.last_name()
                },
                {
                    "property": "website",
                    "value": fake.url()
                },
                {
                    "property": "company",
                    "value": fake.company()
                },
                {
                    "property": "phone",
                    "value": fake.phone_number()
                },
                {
                    "property": "address",
                    "value": fake.street_address()
                },
                {
                    "property": "city",
                    "value": fake.city()
                },
                {
                    "property": "state",
                    "value": fake.state()
                },
                {
                    "property": "zip",
                    "value": fake.zipcode()
                }
            ]
        }

    def setUp(self):
    	self.client = ContactsClient(**helper.get_options())
    	self.contacts = []

    def tearDown(self):
    	""" Cleans up the created objects. """
    	if self.contacts:
    		[self.client.delete_a_contact(contact) for contact in self.contacts]

    @attr('api')
    def test_create_or_update_a_contact(self):
    	""" Test the create or update a contact endpoint is valid. """
    	email = self.test_contact_json['properties'][0]['value']

    	response = self.client.create_or_update_a_contact(email, data=self.test_contact_json)
    	self.assertTrue(len(response) > 0)

    	self.contacts.append(response['vid'])

    @attr('api')
    def test_get_contact_by_email(self):
    	""" Test that the get contact by email address endoint is valid. """
    	email = self.test_contact_json['properties'][0]['value']
    	contact = self.client.create_or_update_a_contact(email, data=self.test_contact_json)['vid']

    	response = self.client.get_contact_by_email(email)
    	self.assertTrue(len(response) > 0)

    	self.contacts.append(contact)

    @attr('api')
    def test_update_a_contact(self):
    	""" Test that the update contact endpoint is valid and that changes persist. """
    	email = self.test_contact_json['properties'][0]['value']
    	contact = self.client.create_or_update_a_contact(email, data=self.test_contact_json)['vid']
    	new_contact_json = self.test_contact_json.copy()
    	new_contact_json['properties'][4]['value'] = new_contact_json['properties'][4]['value'] + ' UPDATED'

    	response = self.client.update_a_contact(contact, data=self.test_contact_json)
    	contact_response = self.client.get_contact_by_email(email)

    	self.assertEqual(contact_response['properties']['company']['value'], new_contact_json['properties'][4]['value'])

    	self.contacts.append(contact)

    @attr('api')
    def test_delete_a_contact(self):
    	""" Test that the delete contact endpoint is valid. """
    	email = self.test_contact_json['properties'][0]['value']
    	contact = self.client.create_or_update_a_contact(email, data=self.test_contact_json)['vid']

    	response = self.client.delete_a_contact(contact)
    	self.assertTrue(len(response) > 0)
