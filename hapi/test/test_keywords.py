import random
import unittest2

import simplejson as json
from nose.plugins.attrib import attr

import helper
from hapi.keywords import KeywordsClient

class KeywordsClientTest(unittest2.TestCase):
    """ Unit tests for the HubSpot Keyword API Python client.

    This file contains some unittest tests for the Keyword API.
    """

    def setUp(self):
        self.client = KeywordsClient(**helper.get_options())
        self.keyword_guids = None
    
    def tearDown(self):
        if (self.keyword_guids):
            map(
                lambda keyword_guid: self.client.delete_keyword(keyword_guid),
                self.keyword_guids
            )
    
    @attr('api')
    def test_get_keywords(self):        
        keywords = self.client.get_keywords()
        self.assertTrue(len(keywords))
        
        print "Got some keywords: %s" % json.dumps(keywords)
    
    @attr('api')
    def test_get_keyword(self):
        keywords = self.client.get_keywords()
        keyword = keywords[0]
        
        result = self.client.get_keyword(keyword['keyword_guid'])
        self.assertEquals(keyword, result)
        
        print "Got a single keywords: %s" % json.dumps(keyword)
    
    @attr('api')
    def test_add_keyword(self):        
        """ Add a test Keyword """
        keyword = 'hapipy_test_keyword%s' % str(random.randint(0,1000))
        result = self.client.add_keyword(keyword)
        
        self.assertEqual(keyword, result['keyword'])
        self.assertTrue(result['keyword_guid'])
        self.keyword_guids = [result['keyword_guid']]

        """ Make sure it's in the list now """
        keywords = self.client.get_keywords()
        
        keywords = filter(lambda x: x['keyword_guid'] == result['keyword_guid'], keywords)
        self.assertTrue(len(keywords) == 1)
        result = keywords[0]
        self.assertTrue(result['keyword'] == keyword)
        
        print "Saved keyword %s" % json.dumps(result)
    
    @attr('api')
    def test_add_keywords(self):
        """ Add multiple Keywords """
        keywords = []
        for i in range(10):
            keywords.append('hapipy_test_keyword%s' % str(random.randint(0,1000)))

        result = self.client.add_keywords(keywords)
        
        self.assertTrue(len(result))
        self.keyword_guids = []
        for keyword in result:
            self.keyword_guids.append(keyword['keyword_guid'])
        
        """ Make sure they're in the list now """
        keywords = self.client.get_keywords()
        
        keywords = filter(lambda x: x['keyword_guid'] in self.keyword_guids, keywords)
        self.assertTrue(len(keywords) == 10)
    
    @attr('api')
    def test_delete_keyword(self):
        keyword = 'hapipy_test_keyword%s' % str(random.randint(0,1000))
        result = self.client.add_keyword(keyword)
        self.client.delete_keyword(result['keyword_guid'])
        
        """ Make sure it's not in the list now """
        keywords = self.client.get_keywords()
        
        keywords = filter(lambda x: x['keyword_guid'] == result['keyword_guid'], keywords)
        self.assertTrue(len(keywords) == 0)
        
        print "Deleted keyword %s" % json.dumps(result)

if __name__ == "__main__":
    unittest2.main()