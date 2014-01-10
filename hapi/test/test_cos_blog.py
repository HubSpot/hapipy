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
    
    # Blogs
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

    # Blog Posts
    @attr('api')
    def test_create_post(self):
        post = self.client.create_post(content_group_id=self.BLOG_ID, name="Test Blog Post")
        pprint(post)
        self.assertTrue(post)

    @attr('api')
    def test_get_posts(self):
        posts = self.client.get_posts(query={'name': 'Demonstration Blog Post'})
        pprint(posts)
        self.assertTrue(posts)

    @attr('api')
    def test_update_post(self):
        post = self.client.update_post(blog_post_id=348109414, name="Updated Test Blog Post")
        pprint(post)
        self.assertTrue(post)

    @attr('api')
    def test_delete_post(self):
        post = self.client.delete_post(blog_post_id=348109414)
        pprint(post)
        self.assertTrue(post)
        post = self.client.undelete_post(blog_post_id=348109414)
        pprint(post)
        self.assertTrue(post)

    @attr('api')
    def test_undelete_post(self):
        post = self.client.undelete_post(blog_post_id=348109414)
        pprint(post)
        self.assertTrue(post)

    @attr('api')
    def test_get_post(self):
        post = self.client.get_post(blog_post_id=348109414)
        pprint(post)
        self.assertTrue(post)

    @attr('api')
    def test_update_auto_save_buffer(self):
        post = self.client.update_auto_save_buffer(blog_post_id=348109414, name="Updated Test Post Buffer")
        pprint(post)
        self.assertTrue(post)

    @attr('api')
    def test_get_auto_save_buffer(self):
        post = self.client.get_auto_save_buffer(blog_post_id=348109414)
        pprint(post)
        self.assertTrue(post)

    @attr('api')
    def test_clone_post(self):
        post = self.client.clone_post(blog_post_id=348109414, name="Cloned Blog Post")
        pprint(post)
        self.assertTrue(post)

if __name__ == "__main__":
    unittest2.main()
