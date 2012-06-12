import unittest2
import helper
import simplejson as json
from nose.plugins.attrib import attr

PORTAL_ID = 62515

class ListsClientTest(unittest2.TestCase):
    """ 
    Unit tests for the HubSpot List API Python wrapper (hapipy) client.
    
    This file contains some unittest tests for the List API.
    
    Questions, comments, etc: http://developers.hubspot.com
    """
    def setUp(self):
        self.client = ListsClient(**helper.get_options())
        
    def tearDown(self):
        pass
        
    @attr('api')
    def test_get_list(self):
        # create a list to get
        dummy_data = json.dumps(dict(
            name = 'try_and_get_me',
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure it was created
        self.asserTrue(len(created_list['lists']))
        
        # the id number of the list the test is trying to get
        id_to_get = created_list['listID']
        
        # try and get it
        recieved_lists = self.client.get_list(id_to_get)
        
        # see if the test got the right list
        self.assertEqual(recieved_lists['lists'][0]['listId'], created_list['listId'])
        
        print "Got this list: %s" % json.dumps(recieved_list['lists'][0])
        
        # clean up
        self.client.delete_list(id_to_get)
        
    @attr('api')
    def test_get_batch_lists(self):
        # holds the ids of the lists being retrieved
        list_ids = []
        
        # make a list to get
        dummy_data = json.dumps(dict(
            name = 'first_test_list',
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure it was actually made
        self.assertTrue(created_list['listID'])
        
        # put the id of the newly made list in list_ids
        list_ids[0] = created_list['listId']
        
        #change the data a little and make another list
        dummy_data['name'] = 'second_test_list'
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure itwas actually made
        self.assertTrue(created_list['listID'])
        
        # put the id number in list_ids
        list_ids[1] = created_list['listId']
        
        # try and get them 
        batch_lists = self.client.get_batch_lists(list_ids)
        
        # make sure you got as many lists as you were searching for
        self.assertEqual(len(list_ids), len(batch_lists['lists']))
        
        # clean up
        self.client.delete_list(list_ids[0])       
        self.client.delete_list(list_ids[1])
        
    @attr('api')
    def test_get_lists(self):
        # try and get lists
        recieved_lists = self.client.get_lists()
        
        # see if the test got at least one
        if len(recieved_lists['lists']) == 0:
            self.fail("Unable to retrieve any lists")
        else:
            print "Got these lists %s" % json.dumps(recieved_lists)
        
    @attr('api')
    def test_get_static_lists(self):
        # create a static list to get
        dummy_data = json.dumps(dict(
            name = 'static_test_list',
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure it was actually made
        self.assertTrue(created_list['listID'])
        
        # this call will return 20 lists if not given another value
        static_lists = self.client.get_static_lists()
        
        if len(static_lists['lists']) == 0:
            self.fail("Unable to retrieve any static lists")
        else:
            print "Found these static lists: %s" % json.dumps(static_lists)
            
            # clean up
            self.client.delete_list(created_list['listId'])
        
    @attr('api')
    def test_get_dynamic_lists(self):
        # make a dynamic list to get
        dummy_data = json.dumps(dict(
            name = 'test_dynamic_list',
            dynamic = True,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure the dynamic list was made
        self.assertTrue(created_list['listId'])
        
        dynamic_lists = self.client.get_dynamic_lists()
        
        if len(dynamic_lists['lists']) == 0:
            self.fail("Unable to retrieve any dynamic lists")
        else:
            print "Found these dynamic lists: %s" % json.dumps(dynamic_lists)
        
            # clean up
            self.client.delete_list(created_list['listId'])

    @attr('api')
    def test_get_list_contacts(self):
        # the id number of the list you want the contacts of
        which_list = 
        
        # try and get the contacts
        contacts = self.client.get_list_contacts(which_list)
        
        # make sure you get at least one
        self.assertTrue(len(contacts['contacts'])
        
        print "Got these contacts: %s from this list: %s" % json.dumps(contacts), which_list
        
    @attr('api')
    def test_get_list_contacts_recent(self):
        # the id number of the list you want the recent contacts of
        which_list = 
        
        recent_contacts = self.client.get_list_contacts_recent(which_list)
        
        if len(recent_contacts['lists']) == 0:
            self.fail("Did not find any recent contacts")
        else:
            print "Found these recent contacts: %s" % json.dumps(recent_conacts)
        
    @attr('api')
    def test_create_list(self):    
        # the data for the list the test is making
        dummy_data = json.dumps(dict(
            list_name = 'test_list',
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        # try and make the list
        created_list = self.client.create_list(dummy_data)
        
        # make sure it was created
        if len(created_lists['lists']) == 0:
            self.fail("Did not create the list")
        else:
            print "Created this list: %s" % json.dumps(created_lists)
            
            # clean up
            self.client.delete_list(created_lists['lists'][0]['listId'])
        
    @attr('api')
    def test_update_list(self):
        # make a list to update
        dummy_data = json.dumps(dict(
            name = 'delete_me',
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure it was actually made
        self.assertTrue(len(created_list['listId']))
        
        # get the id number of the list
        update_list_id = created_list['listId']
        
        # this is the data updating the list
        update_data = json.dumps(dict(
            list_name = 'really_delete_me',
        ))
        
        # try and do the update
        http_response = self.client.update_list(update_list_id, update_data)
        
        if http_response >= 400:
            self.fail("Unable to update list!")
        else:
            print("Updated a list!")
        
        # clean up
        self.client.delete_list(update_list_id)
        
    @attr('api')
    def test_add_contacts_to_list_from_emails(self):
        # make a list to add contacts to
        dummy_data = json.dumps(dict(
            name = 'give_me_contact_emails',
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure it was actually made
        self.assertTrue(len(created_list['lists']))
        
        # the id number of the list being added to
        which_list = created_list['listId']
        
        # the emails of the contacts being added
        emails = json.dumps(dict(
            emails
        ))
        
        # try and add the contacts
        self.client.add_contacts_to_list_from_emails(which_list, emails)
        
    @attr('api')
    def test_add_contact_to_list(self):
        # make a list to add a contact to
        dummy_data = json.dumps(dict(
            name = 'add_a_contact',
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure it was actually made
        self.assertTrue(created_list['listId'])
        
        # the id number of the list the contact is being added to
        which_list = created_list['listId']
        
        # the id number of the contact being added to the list
        which_contact =
        
        added = self.client.add_contact_to_list(which_list, which_contact)
        
        if added['updated'] == which_contact:
            print "Succesfully added contact: %s to list: %s" % which_contact, which_list
            
            # if it worked, clean up
            self.client.delete_list(which_list)
            
        else:
            self.fail("Did not add contact: %s to list: %a" % which_contact, which_list)
        
    @attr('api')
    def test_remove_contact_from_list(self):
        # make a list to remove a contact from
        fake_data = json.dumps(dict(
            name = 'remove_this_contact'
            dynamic = False,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(fake_data)
        
        # make sure it was actually made
        self.assertTrue(created_list['listId'])
        
        # the id number of the list the contact is being deleted from
        which_list = created_list['listId']
        
        # the id number of the contact being deleted
        which_contact = 
        
        # put the contact in the list so it can be removed
        added = self.client.add_contact_to_list(which_list, which_contact)
        
        # make sure it was added
        self.assertTrue(added['updated'])
        
        # try and remove it
        removed = self.client.remove_contact_from_list(which_list, which_contact)
        
        # check if it was actually removed
        if removed['updated'] == which_contact:
            print "Succesfully removed contact: %s from list: %s" % which_contact, which_list
            
            # clean up
            self.client.delete_list(created_list['listId'])
        else:
            self.fail("Did not remove contact %s from list: %s" % which_contact, which_list)
        
    @attr('api')
    def test_delete_list(self):
        # make a list to delete
        dummy_data = json.dumps(dict(
            name = 'should_be_deleted',
            dynamic = False,
            portalId = PORTAL_ID

        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # check if it was actually made
        self.assertTrue(created_list['listId'])
        
        # the id number of the list being deleted
        id_to_delete = created_list['listId']
        
        # try deleting it
        self.client.delete_list(id_to_delete)
        
        # try and get the list that should have been deleted
        check = self.client.get_list(id_to_delete)
        
        # check should not have any lists
        self.assertEqual(len(check['lists']), 0)
        
        print "Sucessfully deleted a test list"
        
    @attr('api')
    def test_refresh_list(self):
        # make a dynamic list to refresh
        dummy_data = json.dumps(dict(
            name = 'refresh_this_list',
            dynamic = True,
            portalId = PORTAL_ID
        ))
        
        created_list = self.client.create_list(dummy_data)
        
        # make sure it actually made the list
        self.assertTrue(created_list['listId'])
        
        # do the refresh
        refresh_response = self.client.refresh_list(created_list['listId'])
        
        # check if it worked
        if refresh_response >= 400:
            self.fail("Failed to refresh list: %s" % json.dumps(created_list))
        else:
            print "Succesfully refreshed list: %s" % json.dumps(created_list)
            
            # clean up
            self.client.delete_list(created_list['listId'])   

if __name__ == "__main__":
    unittest2.main()