import unittest2
import helper
import logger
from pprint import pprint
import simplejson as json
from hapi.cos_blog import COSBlogClient
from nose.plugins.attrib import attr

class BlogClientTest(unittest2.TestCase):
    """ 
    Unit tests for the HubSpot Blog API Python wrapper (hapipy) client.
    
    This file contains some unittest tests for the Blog API.
    
    Questions, comments, etc: http://docs.hubapi.com/wiki/Discussion_Group
    """
    BLOG_ID = 351076997
    VERSION_ID = 12926383
    
    def setUp(self):
        self.client = COSBlogClient(**helper.get_options())
    
    def tearDown(self):
        pass
    
    @attr('api')
    def test_get_blogs(self):
        blogs = self.client.get_blogs()
        self.assertTrue(len(blogs))
        pprint(blogs)

    @attr('api')
    def test_get_blog(self):
        blog = self.client.get_blog(self.BLOG_ID)
        self.assertTrue(blog)
        self.assertTrue(blog['id'] == self.BLOG_ID)
        pprint(blog)

    @attr('api')
    def test_get_blog_versions(self):
        versions = self.client.get_blog_versions(self.BLOG_ID)
        self.assertTrue(versions)
        pprint(versions)

    @attr('api')
    def test_get_blog_version(self):
        version = self.client.get_blog_version(self.BLOG_ID, self.VERSION_ID)
        self.assertTrue(version)
        pprint(version)

if __name__ == "__main__":
    unittest2.main()
