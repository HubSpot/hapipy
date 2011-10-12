from base import BaseClient
from xml.dom import minidom

BLOG_API_VERSION = '1'

class BlogClient(BaseClient):
  
    def _get_path(self, subpath):
        return 'blog/v%s/%s' % (BLOG_API_VERSION, subpath)
    
    def get_blogs(self, **options):
        return self._call('list.json', **options)
    
    def get_blog_info(self, blog_guid, **options):
        return self._call(blog_guid, **options)
    
    def get_posts(self, blog_guid, **options):
        return self._call('%s/posts.json' % blog_guid, **options)
    
    def get_draft_posts(self, blog_guid, **options):
        return self._call('%s/posts.json' % blog_guid, params={'draft': 'true'}, **options)

    def get_pulished_posts(self, blog_guid, **options):
        return self._call('%s/posts.json' % blog_guid, params={'draft': 'false'}, **options)
    
    def get_blog_comments(self, blog_guid, **options):
        return self._call('%s/comments.json' % blog_guid, **options)
    
    def get_post(self, post_guid, **options):
        return self._call('posts/%s.json' % post_guid, **options)
    
    def get_post_comments(self, post_guid, **options):
        return self._call('posts/%s/comments.json' % post_guid, **options)
    
    def get_comment(self, comment_guid, **options):
        return self._call('comments/%s.json' % comment_guid, **options)
    
    def create_post(self, blog_guid, author_name, author_email, title, summary, content, tags, **options):
        tag_xml = ''
        for tag in tags:
            tag_xml += '<category term="tag %s" />' % tag
        post = '''<?xml version="1.0" encoding="utf-8"?>
                <entry xmlns="http://www.w3.org/2005/Atom">
                    <title>%s</title>
                    <author>
                        <name>%s</name>
                        <email>%s</email>
                    </author>
                    <summary>%s</summary>
                    <content type="html"><![CDATA[%s]]></content>
                    %s
                </entry>''' % (title, author_name, author_email, summary, content, tag_xml)
        raw_response = self._call('%s/posts.atom' % blog_guid, data=post, method='POST', content_type='application/atom+xml', raw_output=True, **options)
        return minidom.parseString(raw_response).id
    
    def update_post(self, post_guid, title, summary, content, meta_desc, meta_keyword, tags, **options):
        tag_xml = ''
        for tag in tags:
            tag_xml += '<category term="tag %s" />' % tag
        post = '''<?xml version="1.0" encoding="utf-8"?>
                <entry xmlns="http://www.w3.org/2005/Atom" xmlns:hs="http://www.hubspot.com/">
                    <title>%s</title>
                    <summary>%s</summary>
                    <content type="text">%s</content>
                    %s
                    <hs:metaDescription>%s</hs:metaDescription>
                    <hs:metaKeywords>%s</hs:metaKeywords>
                </entry>''' % (title, summary, content, tag_xml, meta_desc, meta_keyword)
        raw_response = self._make_request('posts/%s.atom' % post_guid, content_type='application/atom+xml', data=post, method='PUT', raw_output=True, **options)
        return minidom.parseString(raw_response).id
    
    def publish_post(self, post_guid, publish_time, is_draft, should_notify, **options):
        post = '''<?xml version="1.0" encoding="utf-8"?>
                <entry xmlns="http://www.w3.org/2005/Atom" xmlns:hs="http://www.hubspot.com/">
                    <published>%s</published>
                    <hs:draft>%s</hs:draft>
                    <hs:sendNotifications>%s</hs:sendNotifications>
                </entry>''' % (publish_time, is_draft, should_notify)
        raw_response = self._make_request('posts/%s.atom' % post_guid, content_type = 'application/atom+xml', data=post, method='PUT', raw_output=True, **options)
        return minidom.parseString(raw_response).id
    
    def create_comment(self, post_guid, author_name, author_email, author_uri, content, **options):
        post = '''<?xml version="1.0" encoding="utf-8"?>
                <entry xmlns="http://www.w3.org/2005/Atom">
                    <author>
                    <name>%s</name>
                    <email>%s</email>
                    <uri>%s</uri>
                    </author>
                    <content type="html"><![CDATA[%s]]></content>
                </entry>''' % (author_name, author_email, author_uri, content)
        raw_response = self._make_request('posts/%s/comments.atom' % post_guid, content_type='application/atom+xml', data=post, method='POST', raw_output=True, **options)
        return minidom.parseString(raw_response).id
    

