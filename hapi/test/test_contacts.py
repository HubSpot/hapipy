import unittest2
import helper
import simplejson as json
from nose.plugins.attrib import attr

class ContactsClientTest(unittest2.TestCase):
    """ Unit tests for the HubSpot Clients API Python client.

    This file contains some unittest tests for the Clients API.

    It is not intended to be exhaustive, just simple exercises and
    illustrations.
    
    All these methods work in similar ways. First, make a variable with
    required input. Pass it into the method being tested. Check if that
    method returned something. Display results. Clean up.

    Additional tests and other improvements welcome.

    TODO: these tests have not been run before, so they may not pass

    Questions, comments, etc: http://docs.hubapi.com/wiki/Discussion_Group
    """
    
    def setUp(self):
        self.client = ContactsClient(**helper.get_options())
    
    def tearDown(self):
        pass

    @attr('api')
    def test_get_contact(self):
        # make a contact to mess with
        dummy_contact = json.dumps(dict(
            email = 'blaghblagh@blagh.com',
            firstname = 'Robert',
            lastname = 'Paulson',
            website = 'www.wxyz.com'
            company = 'Paper Street Soap Company',
            phone = '1369121518',
            city = 'Anytown',
            state = 'The moon',
            zip = 'space'
        ))
        
        created_contacts = self.client.create_contact(dummy_contact)
        
        # this is the contact's id the test will look for
        test_id = created_contacts['vid']
        
        # try and get it
        contacts_recieved = self.client.get_contact(test_id)
        
        # make sure you got at least one contact
        self.assertTrue(contacts_recieved['vid'])
        
        print "Got these contacts by their id: %s" % json.dumps(contacts_recieved)
    
    @attr('api')
    def test_get_contact_by_email(self):
        # create a contact to get
        dummy_contact = json.dumps(dict(
            email = 'yetAnother@fakeEmail.com',
            firstname = 'Imaginary',
            lastname = 'Friend',
            website = 'nonexistant.com',
            company = 'Unproductive Corp',
            phone = '1231231231',
            address = '25 Danger road',
            city = 'Stormwind',
            state = 'Azeroth',
            zip = '71200'
        ))
        
        returned_contact = self.client.create_contact(dummy_contact)
        
        # make sure it was actually made
        self.assertTrue(returned_contact['vid'])
        
        # this is the contact's email the test will be looking for
        test_email = returned_contact['email']
        
        # try and get it
        contacts_recieved = self.client.get_by_email(test_email)
        
        # see if you got something
        self.assertTrue(contacts_recieved['vid'])
        
        print "Got these contacts by their email: %s" % json.dumps(contacts_recieved)
            
        # if it found it, clean up
        self.client.delete_contact(contacts_recieved['vid'])
    
    @attr('api')
    def test_create_contact(self):
        """I am unsure if this is the correct way to make the contact's information in json"""
        # this will be the information of the contact being made. It is JSON, as required according to the API
        dummy_contact = json.dumps(dict(
            email = 'silly@thisisntreal.com', 
            firstname = 'Silly', 
            lastname = 'Testman', 
            website = 'thisisntreal.com', 
            company = 'Fake Industries', 
            phone = '1234567890', 
            address = '123 fake street', 
            city = 'Springfield',
            state = 'Ohiyamaude',
            zip = '12345'
            ))
        
        # try and make it
        created_contact = self.client.create_contact(dummy_contact)
        
        # see if you made it
        self.assertTrue(created_contact['vid'])
            print "Created a contact: %s" % json.dumps(created_contact)
            
            # if it was made, clean up
            self.client.archive_contact(created_contact['vid'])
        else:
            self.fail("Was not able to create a contact: %s" % json.dumps(dummy_contact))
    
    @attr('api')
    def test_update_contact(self):
        # make a contact to update
        fake_info = json.dumps(dict(
            email = 'old.email@thisisntreal.com',
            firstname = 'Dumb',
            lastname = 'Testman',
            website = 'foobar.com',
            company = 'Acme Inc',
            phone = '1357111317'
            address = '5678 Whatever street',
            city = 'Pretendville',
            state = 'Imaginationland',
            zip = '31337'
        ))
        
        created_contact = self.client.create_contact(fake_info)
        
        # the contact's id number the test will try to update
        contact_id_to_update = created_contact['vid']
        
        # the information being updated in the contact
        new_fake_info = json.dumps(dict(
            email = 'new.email@thisisntreal.com',
            firstname = 'Stupid',
            lastname = 'Testguy',
            website = 'thisisfake.org'
            company = 'Pretend Incorporated',
            phone = '0987654321',
            address = '321 Sesame Street',
            city = 'Atlantis',
            state = 'Atlantic Ocean',
            zip = '11235'
        ))
        
        # try and update
        update_response = self.client.update_client(contact_to_update, new_fake_info)
        
        # make sure it worked
        if update_response >= 400:
            self.fail("Unable to update contact")
        else:
            print "Succesfully updated a contact"
            
            # if it worked, clean up
            self.client.archive_contact(contact_to_update)
    
    @attr('api')
    def test_archive_contact(self):
        # make a contact to archive
        fake_info = json.dumps(dict(
            email = 'person@emailserver.com',
            firstname = 'Scumbag',
            lastname = 'Steve',
            website = 'examplewebsite.edu',
            company = 'Spatula City',
            phone = '900014255',
            address = '1600 Pensylvania ave',
            city = 'Washington D.C.',
            state = 'Not really sure',
            zip = '43110'
        ))
        
        created_contact = self.client.create_contact(fake_info)
        
        # make sure it was actually created
        self.assertTrue(created_contact['vid'])
        
        # the id number of the contact being deleted
        id_to_archive = created_contact['vid']
        
        # try and archive
        self.client.delete_archive(id_to_delete)
        
        # look for the archived id
        found_contacts = self.client.get_contact(id_to_archive)
        
        # it should not have been returned
        if len(found_contacts['contacts']) == 0:
            print "The contact with id: %s was archived" % id_to_archive
        else:
            self.fail("Was not able to archive contact %s" % id_to_archive)
    
    @attr('api')
    def test_get_statistics(self):
        # retrieve the statistics
        returned_stats = self.client.get_statistics()
        
        # make sure you got something
        self.assertTrue(len(returned_statistics))
        
        print "Got stats: %s" % json.dumps(returned_stats)
    
    @attr('api')
    def test_search(self):
        # make a contact to search for
        fake_info = json.dumps(dict(
            email = 'notreal@examplecontact.com',
            firstname = 'Troll',
            lastname = 'Face',
            website = 'www.blaghblaghblagh.com',
            company = 'Initech',
            phone = '1098765432',
            address = '52 Last Avenue',
            city = 'Leftraod',
            state = 'Energy',
            zip = '56473'
        ))
        
        created_contact = self.client.create_contact(fake_info)
        
        # make sure it was actually made
        self.assertTrue(len(created_contact['vid']))
        
        # what the test is searching for
        search_this = 'Troll'
        
        # do the search
        returned_contacts = self.client.search(search_this)
        
        # the search should return at least one contact
        if len(returned_contacts['contacts']) == 0:
            print "Didn't find anything by searching: %s" % search_this
        else:
            print "Found these contacts: %s" % json.dumps(returned_contacts)

if __name__ == "__main__":
    unittest2.main()
