import sys
import time
import random
import unittest
import datetime
import pdb

from pyspot import *
from django.utils import simplejson

API_KEY = '686ec9d0-b3d0-11e0-ae57-123139078537'

PORTAL_ID = 73154

class pyspot_UnitTests(unittest.TestCase):
  def setUp(self):
    pass
  
  def tearDown(self):
    pass
    
  def xtest_blog_info(self):
    # run through some basic Blog client tests
    blog_client = HubSpotBlogClient(API_KEY)
    blogs = blog_client.get_blogs()
    self.assertEquals(blogs.get('status'), 200)
    print '\nRESULT: Retrieved %s blogs.\n' % str(len(blogs.get('body')))
    
    blog = blogs.get('body')[0]
    blog_guid = blog.get('guid')
    self.assertNotEquals(blog_guid, None)
    blog_details = blog_client.get_blog(blog_guid)
    self.assertEquals(blog_details.get('status'), 200)
    print 'RESULT: Got some details for blog %s\n' % blog_guid

  def xtest_blog_pub(self):
    # create and modify blog content
    blog_client = HubSpotBlogClient(API_KEY)  
    blogs = blog_client.get_blogs()
    blog = blogs.get('body')[0]
    blog_guid = blog.get('guid')  
    author_name = 'CTOD'
    author_email = 'codonnell@hubspot.com'
    title = 'Test blog post %s' % datetime.datetime.now()
    summary = 'summary'
    content = 'blog post content'
    tags = ['tagone', 'tag two']
    
    new_post = blog_client.create_post(blog_guid, author_name, author_email, title, summary, content, tags)
    self.assertEquals(new_post.get('status'), 200)
    post_guid = new_post.get('body').get('guid')
    print 'RESULT: Posted blog post %s\n' % post_guid
    
  def xtest_keywords(self):
    kw_client = HubSpotKeywordClient(API_KEY, PORTAL_ID)
    
    # get all keywords
    print '\nGetting all keywords for portal %d' % PORTAL_ID
    keywords = kw_client.get_keywords()
    total_keywords = len(keywords.get('body').get('keywords'))
    self.assertEquals(keywords.get('status'), 200)
    print 'RESULT: Got %s keywords back.' % str(total_keywords)
    
    # get a keyword
    keyword_guid = keywords.get('body', {}).get('keywords', {})[0].get('keyword_guid')
    print '\nGetting data for individual keyword (guid: %s)' % simplejson.dumps(keyword_guid)
    keyword = kw_client.get_keyword(keyword_guid)
    self.assertEquals(keyword.get('status', None), 200)
    print 'RESULT: Got keyword details on: %s\n\n%s' % (keyword.get('body').get('keyword'), keyword.get('body'))
    
    # add a keyword
    kw = 'pyspot_test_keyword_%s' % str(random.randint(0,1000))
    print '\nAttempting to add %s to the database' % kw
    try:
        new_keyword = kw_client.add_keyword(kw)
        self.assertEqual(new_keyword.get('status'), 201)
        keyword_guid = new_keyword.get('body').get('keyword_guid')
        keywords = kw_client.get_keywords()
        self.assertEqual(len(keywords.get('body').get('keywords')), total_keywords+1)
        print 'RESULT: Added keyword: %s' % kw
    except (AssertionError):
        print 'ERROR: Failed to add keyword: %s' % kw
    
    # try to re-add the same keyword
    retried_keyword = kw_client.add_keyword(kw)
    self.assertEqual(retried_keyword.get('status'), 500)
    print 'RESULT: Tried to re-add same keyword and failed (this is good)'
    
    # get the new keyword
    new_kw = kw_client.get_keyword(keyword_guid)
    self.assertEqual(new_kw.get('body').get('keyword_guid'), keyword_guid)
    print 'RESULT: got new keyword details'
    
    # refresh the keyword
    refreshed = kw_client.refresh_keyword(keyword_guid)
    self.assertEqual(refreshed.get('status'), 200)
    print 'RESULT: refreshed keyword'
    
    # delete the keyword
    deleted = kw_client.delete_keyword(keyword_guid)
    self.assertEqual(deleted.get('status'), 200)
    
    # verify deletion
    deleted = kw_client.get_keyword(keyword_guid)
    self.assertNotEqual(deleted.get('status'), 200)
    print 'RESULT: keyword deleted'
    
    # refresh all keywords
    refreshed = kw_client.refresh_all_keywords()
    self.assertEqual(refreshed.get('status'), 200)
    print 'RESULT: all keywords refreshed'
    
    # get suggestions based on a keyword
    kw = 'pyspot_test_%s' % str(random.randint(0,1000))
    print '\nGetting results based on the keyword: %s' % kw
    suggested = kw_client.get_suggestions(kw, {})
    self.assertEqual(suggested.get('status'), 200)
    print 'RESULT: returned the following suggestions:\n%s' % suggested

  def xtest_get_events(self):
    event_client = HubSpotEventClient(API_KEY)
    events = event_client.get_events()
    self.assertEquals(events.get('status'), 200)
    total_events = len(events.get('body'))
    print '\nGot %s events back' % str(total_events)
  
  def xtest_crud_events(self):
    event_client = HubSpotEventClient(API_KEY)
    description = 'pyspot test event %s' % datetime.datetime.now()
    create_date = str(int(time.time()*1000))
    url = 'http://hubspot.com/test-event'
    event_type= 'api wrapper test'
    new_event = event_client.create_event(description, create_date, url, event_type)
    self.assertEquals(new_event.get('status'), 201)
    
    events = event_client.get_events()
    new_total_events = len(events.get('body'))
    self.assertEquals(new_total_events, total_events + 1)
    
  def xtest_lead_callbacks(self):
    lead_client = HubSpotLeadsClient(API_KEY)
    callback_urls = lead_client.get_callback_urls()
    self.assertEquals(callback_urls.get('status'), 200)
    total_urls = len(callback_urls.get('body'))
    print '\nGot %s callback urls' % str(total_urls)
    
    test_url = 'https://www.postbin.org/1iz1qw0?test=%s' % str(int(time.time()*1000))
    new_url = lead_client.register_callback_url(test_url)
    self.assertEquals(new_url.get('status'), 201)
    print '\nAdded a new callback URL successfully'
    
    callback_urls = lead_client.get_callback_urls()
    self.assertEquals(callback_urls.get('status'), 200)
    new_total_urls = len(callback_urls.get('body'))
    self.assertEquals(new_total_urls, total_urls + 1)
    print '\nVerified there is 1 more callback url than before'
  
  def xtest_leads(self):
    lead_client = HubSpotLeadsClient(API_KEY)
    
    # search for leads
    leads = lead_client.search_leads('judy', {})
    self.assertEquals(leads.get('status'), 200)
    print '\nFound a lead! Guid: %s' % leads.get('body')[0].get('guid')
    
    
    # create a lead
    
    # get the new lead
    
    # close the new lead
    
    # verify closed
    
    # create the lead again
    

if __name__ == "__main__":
  # Build the test suite
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(pyspot_UnitTests))

  # Execute the test suite
  print("Testing pyspot\n")
  result = unittest.TextTestRunner(verbosity=2).run(suite)
  sys.exit(len(result.errors) + len(result.failures))
