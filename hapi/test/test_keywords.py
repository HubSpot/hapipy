# coding: utf-8
import random
import unittest2

import simplejson as json
from nose.plugins.attrib import attr

import helper
from hapi.keywords import KeywordsClient

class KeywordsClientTest(unittest2.TestCase):
    """ Unit tests for the HubSpot Keyword API Python client.

    This file contains some unittest tests for the Keyword API.

    Questions, comments: http://docs.hubapi.com/wiki/Discussion_Group
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
        
        print "\n\nGot some keywords: %s" % json.dumps(keywords)
    
    @attr('api')
    def test_get_keyword(self):
        keywords = self.client.get_keywords()
        if len(keywords) < 1:
            self.fail("No keywords available for test.")

        keyword = keywords[0]
        print "\n\nGoing to get a specific keyword: %s" % keyword
        
        result = self.client.get_keyword(keyword['keyword_guid'])
        self.assertEquals(keyword, result)
        
        print "\n\nGot a single matching keyword: %s" % keyword['keyword_guid']
    
    @attr('api')
    def test_add_keyword(self):        
        # Add a single keyword to this account,
        keyword = 'hapipy_test_keyword%s' % str(random.randint(0,1000))
        result = self.client.add_keyword(keyword)
        print "\n\nAdded keyword: %s" % json.dumps(result)
        
        keywords = result['keywords']
        first_keyword = keywords[0]
        self.assertEqual(keyword, first_keyword['keyword'])
        self.assertTrue(first_keyword['keyword_guid'])
        self.keyword_guids = [first_keyword['keyword_guid']]

        # Make sure it's in the list now
        keywords = self.client.get_keywords()
        
        keywords = filter(lambda x: x['keyword_guid'] == first_keyword['keyword_guid'], keywords)
        self.assertEqual(len(keywords), 1)
        result = keywords[0]
        self.assertTrue(result['keyword'] == keyword)
        
        print "\n\nSaved keyword %s" % json.dumps(result)
    
    @attr('api')
    def test_add_keywords(self):
        # Add multiple Keywords in one API call.
        keywords = []
        for i in range(10):
            keywords.append('hapipy_test_keyword%s' % str(random.randint(0,1000)))

        result = self.client.add_keywords(keywords)
        
        self.assertTrue(len(result))
        self.keyword_guids = []
        for keyword in result:
            self.keyword_guids.append(keyword['keyword_guid'])
        
        # Make sure they're in the list now
        keywords = self.client.get_keywords()
        
        keywords = filter(lambda x: x['keyword_guid'] in self.keyword_guids, keywords)
        self.assertEqual(len(keywords), 10)

        print "\n\nAdded multiple keywords: %s" % keywords
    
    @attr('api')
    def test_delete_keyword(self):
        # Delete multiple keywords in one API call.
        keyword = 'hapipy_test_keyword%s' % str(random.randint(0,1000))
        result = self.client.add_keyword(keyword)
        keywords = result['keywords']
        first_keyword = keywords[0]
        print "\n\nAbout to delete a keyword, result= %s" % json.dumps(result)

        self.client.delete_keyword(first_keyword['keyword_guid'])
        
        # Make sure it's not in the list now
        keywords = self.client.get_keywords()
        
        keywords = filter(lambda x: x['keyword_guid'] == first_keyword['keyword_guid'], keywords)
        self.assertTrue(len(keywords) == 0)
        
        print "\n\nDeleted keyword %s" % json.dumps(first_keyword)
        
    @attr('api')
    def test_utf8_keywords(self):
        # Start with base utf8 characters
        # TODO: Fails when adding simplified chinese char: 广 or cyrillic: л
        utf8_keyword_bases = ['é', 'ü']

        keyword_guids = []
        for utf8_keyword_base in utf8_keyword_bases:
            original_keyword = '%s - %s' % (utf8_keyword_base, str(random.randint(0,1000)))
            result = self.client.add_keyword(original_keyword)
            print "\n\nAdded keyword: %s" % json.dumps(result)
            print result

            keywords_results = result.get('keywords')
            keyword_result = keywords_results[0]

            self.assertTrue(keyword_result['keyword_guid'])
            keyword_guids.append(keyword_result['keyword_guid'])

            actual_keyword = keyword_result['keyword']

            # Convert to utf-8 to compare strings. Returned string is \x-escaped
            if isinstance(original_keyword, unicode):
                original_unicode_keyword = original_keyword
            else:
                original_unicode_keyword = original_keyword.decode('utf-8')

            if isinstance(actual_keyword, unicode):
                actual_unicode_keyword = actual_keyword
            else:
                actual_unicode_keyword = actual_keyword.decode('utf-8')

            self.assertEqual(actual_unicode_keyword, original_unicode_keyword)

if __name__ == "__main__":
    unittest2.main()