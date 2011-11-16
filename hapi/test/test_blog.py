import unittest2
import helper
import logger
import simplejson as json
from hapi.blog import BlogClient
from nose.plugins.attrib import attr

class BlogClientTest(unittest2.TestCase):
    """ 
    Unit tests for the HubSpot Blog API Python wrapper (hapipy) client.
    
    This file contains some unittest tests for the Blog API.
    
    Questions, comments, etc: http://docs.hubapi.com/wiki/Discussion_Group
    """
    
    def setUp(self):
        self.client = BlogClient(**helper.get_options())
    
    def tearDown(self):
        pass
    
    @attr('api')
    def test_get_blogs(self):
        blogs = self.client.get_blogs()
        self.assertTrue(len(blogs))
        print "Got some blogs from the portal: GUID: %s" % json.dumps(blogs)
    
    @attr('api')
    def test_get_blog_info(self):
        blogs = self.client.get_blogs()
        blog = blogs[0]
        
        blog_info = self.client.get_blog_info(blog['guid'])
        self.assertTrue(len(blog_info))
        print "Got some blog info about a blog: %s" % json.dumps(blog_info)
    
    @attr('api')
    def test_get_posts(self):
        blogs = self.client.get_blogs()
        blog = blogs[0]
        
        blog_posts = self.client.get_posts(blog['guid'])
        self.assertTrue(len(blog_posts))
        print "Got some blog posts from the blog: GUID: %s" % json.dumps(blog_posts)
    
    @attr('api')
    def test_get_draft_posts(self):
        blogs = self.client.get_blogs()
        blog = blogs[2]
        
        blog_posts = self.client.get_draft_posts(blog['guid'])
        self.assertTrue(len(blog_posts))
        print "Got some draft blog posts from the blog: %s" % json.dumps(blog_posts)
    
    @attr('api')
    def test_get_published_posts(self):
        blogs = self.client.get_blogs()
        blog = blogs[0]
        
        blog_posts = self.client.get_pulished_posts(blog['guid'])
        self.assertTrue(len(blog_posts))
        print "Got some published blog posts from the blog: %s" % json.dumps(blog_posts)
    
    @attr('api')
    def test_get_blog_comments(self):
        blogs = self.client.get_blogs()
        blog = blogs[0]
        
        blog_comments = self.client.get_blog_comments(blog['guid'])
        self.assertTrue(len(blog_comments))
        print "Got some comments from the blog: %s" % json.dumps(blog_comments)
    
    @attr('api')
    def test_get_post(self):
        blogs = self.client.get_blogs()
        blog = blogs[0]
        posts = self.client.get_posts(blog['guid'])
        post = posts[0]
        
        blog_post = self.client.get_post('6a0626c6-98f1-4b7c-a3c0-0b5a1daabf2b')
        self.assertTrue(len(blog_post))
        print "Got a blog post: %s" % json.dumps(blog_post)
    
    @attr('api')
    def test_get_post_comments(self):
        blog_post_comment = self.client.get_post_comments('c34d2900-ec96-4674-97d3-ddae2d2669f0')
        self.assertTrue(len(blog_post_comment))
        print "Got post comments: %s" % json.dumps(blog_post_comment)
    
    @attr('api')
    def test_get_comment(self):
        blogs = self.client.get_blogs()
        blog = blogs[0]
        comments = self.client.get_blog_comments(blog['guid'])
        comment = comments[0]
        
        blog_comment = self.client.get_comment(comment['guid'])
        self.assertTrue(len(blog_comment))
        print "Got a post comment: %s" % json.dumps(blog_comment)
    
    @attr('api')
    def test_create_post(self):
        blogs = self.client.get_blogs()
        blog = blogs[0]
        post_to_create = self.client.create_post(blog['guid'], 'Test Author', 'testapi@hubspot.com', 'I am a test post', 'This is a test summary', '<b>This is the content of the blog post</b>', ['tag1', 'tag2'])
        self.assertTrue(post_to_create)
        post = post_to_create.toprettyxml()
        print "Created a blog post: %s" % post
    
    @attr('api')
    def test_update_post(self):
        post_to_update = self.client.update_post('6a0626c6-98f1-4b7c-a3c0-0b5a1daabf2b', 'I am a test post title UPDATED', 'This is a test summary', '<b>This is the content of the blog post updated</b>', 'meta desc updated', ['keyword1', 'keyword2'], ['tag1', 'tag2', 'tag4'])
        self.assertTrue(post_to_update)
        post = post_to_update.toprettyxml()
        print "Updated a blog post: %s" % post
    
    @attr('api')
    def test_publish_post(self):
        now = "2100-03-20T10:10:00Z"
        post_to_publish = self.client.publish_post('6a0626c6-98f1-4b7c-a3c0-0b5a1daabf2b', now, 0, 0)
        self.assertTrue(post_to_publish)
        post = post_to_publish.toprettyxml()
        print "Published a blog post: %s" % post
    
    @attr('api')
    def test_create_comment(self):
        comment = self.client.create_comment('6a0626c6-98f1-4b7c-a3c0-0b5a1daabf2b', 'Test Comment Author', 'testapi@hubspot.com', 'http://hubspot.com', 'I am a test comment')
        self.assertTrue(comment)
        posted_comment = comment.toprettyxml()
        print "Published a blog post: %s" % posted_comment
    
    
if __name__ == "__main__":
    unittest2.main()

