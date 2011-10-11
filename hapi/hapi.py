#!/usr/bin/env python
#
# Copyright 2011 HubSpot Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "markitecht (Christopher O'Donnell)"
__author__ = "adrianmott (Adrian Mott)"
__author__ = "Matt Furtado"
__author__ = "prior (Michael Prior)"
__author__ = "jessbrandi (Jessica Scott)"

import re
import hmac
import base64
import urllib
import httplib
import logging
import time
from xml.dom import minidom
from blog_objects import *
from lead_objects import *
from lead_nurturing_objects import *

try:
    import hashlib
except ImportError:
    import md5 as hashlib

try:
    import json as simplejson
    simplejson.loads
except (ImportError, AttributeError):
    try:
        import simplejson
        simplejson.loads
    except (ImportError, AttributeError):
        try:
            from django.utils import simplejson
            simplejson.loads
        except (ImportError, AttributeError):
            try:
                import jsonlib as simplejson
                simplejson.loads
            except:
                pass

HUBSPOT_BLOG_API_VERSION = '1'
HUBSPOT_LEADS_API_VERSION = '1'

class HubSpotClient(object):
    '''Client for interacting with the HubSpot APIs'''
    
    def __init__(self, api_key, timeout=10, **extra_options):
        self.api_key = api_key
        self.options = {'timeout':timeout, 'api_base':'hubapi.com'}
        self.options.update(extra_options)
        self._prepare_connection_type()

    def _prepare_connection_type(self):
        connection_types = {'http': httplib.HTTPConnection, 'https': httplib.HTTPConnection}
        parts = self.options['api_base'].split('://')
        protocol = (parts[0:-1]+['https'])[0]
        self.options['connection_type'] = connection_types[protocol]
        self.options['api_base'] = parts[-1]

    def _create_path(self, subpath):
        raise Exception("Unimplemented _create_path for HubSpotClient subclass!")
    
    def _prepare_response(self, code, data):
        msg = self._get_msg(code)
        if data:
            try:
                data = simplejson.loads(data)
            except ValueError:  
                pass
        return {'status': code, 'body': data or {}, 'msg': msg}
    
    def _get_msg(self, code):  # need to get a message here?
        return None
    
    def _make_request(self, subpath, params=None, method='GET', data=None, **options):
        opts = self.options.copy()
        opts.update(options)

        conn = opts['connection_type'](opts['api_base'], timeout=opts['timeout'])

        ## what is this all about!?? -mp -- not getting it...
        if data and not isinstance(data, str):
            if method != 'PUT':  #and method doesn't contain 'blog'...this will hose update lead !!!!
                data = urllib.urlencode(data)

        params = params or {}
        params['hapikey'] = self.api_key
        if opts.get('hub_id') or opts.get('portal_id'):
            params['portalId'] = opts.get('hub_id') or opts.get('portal_id')
        url = opts.get('url') or '/%s?%s' % (self._create_path(subpath), urllib.urlencode(params))
        headers = {'Content-Type': opts.get('content_type') or 'application/json'}
        conn.request(method, url, data, headers)
        result = conn.getresponse()
        body = {}
        if result.status < 400:
            body = result.read()
        else:
            logging.error('Client request error. Code: %s - Reason: %s - URL: %s' % (str(result.status), result.reason, url))
        conn.close()
        return self._prepare_response(result.status, body)
    

class HubSpotLeadsClient(HubSpotClient):
    """
    The PySpot Leads client uses the _make_request method to call the API for data.  It returns only JSON in the standard format:
    { status: 'status', body: 'data from API call', msg: 'message' }
    PLEASE NOTE that the 'body' here is decoded JSON.
    """
    def _create_path(self, subpath):
        return 'leads/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, subpath)
  
    def get_lead(self, lead_guid, **options):
        response = self._make_request('list/', params={'guids[0]': lead_guid}, **options)
        indv_lead = Lead(response['body'][0])
        return indv_lead
    
    def search_leads(self, search_value, **options):
        response = self._make_request('list/', params={'search': search_value}, **options)
        lead_objs = []
        for indv_leads in response['body']:
            indv_lead_obj = Lead(indv_leads)
            lead_objs.append(indv_lead_obj)
        return lead_objs
    
    def update_lead(self, lead_guid, update_data={}, **options):
        response = self._make_request('lead/%s/' % lead_guid, data=str(update_data), method='PUT', **options)
        if response['status'] == 200:
            lead_response = self._make_request('list/', params={'guids[0]': lead_guid}, **options)
            indv_lead = Lead(lead_response['body'][0])
            return indv_lead
    
    def offset_leads(self, offset, **options):
        response = self._make_request('list/', params={'offset': offset}, **options)
        lead_objs = []
        for indv_leads in response['body']:
            indv_lead_obj = Lead(indv_leads)
            lead_objs.append(indv_lead_obj)
        return lead_objs
    
    def get_webhook(self, **options):  #WTF are these 2 methods for?
        return self._make_request('callback-url', **options)
    
    def register_webhook(self, url, **options):
        return self._make_request('callback-url', params={'url': url}, data={'url': url}, method='POST', **options)
    
    def close_lead(self, lead_guid, close_time=None, **options):
        if close_time == None:
            now = int(time.time()*1000)
            data = "{'guid':'%s', 'closedAt': '%s'}" % (lead_guid, now)
        else:
            data = "{'guid':'%s', 'closedAt': '%s'}" % (lead_guid, close_time)
        response = self._make_request('lead/%s/' % lead_guid, data=str(data), method='PUT', **options)
        if response['status'] == 200:
            lead_response = self._make_request('list/', params={'guids[0]': lead_guid}, **options)
            indv_lead = Lead(lead_response['body'][0])
            return indv_lead
    

class HubSpotLeadNurtureClient(HubSpotClient):
  
    def _create_path(self, subpath):
        return 'nurture/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, subpath)
    
    def get_campaigns(self, **options):
        response = self._make_request('campaigns', **options)
        ln_campaigns = []
        for lnc in response['body']:
            lnc_obj = LeadNurturingCampaign(lnc)
            ln_campaigns.append(lnc_obj)
        return ln_campaigns
    
    def get_leads(self, campaign_guid, **options):
        response = self._make_request('campaign/%s/list' % campaign_guid, **options)
        leads_in_campaign = []
        for leads in response['body']:
            leads_in_ln = CampaignLeads(leads)
            leads_in_campaign.append(leads_in_ln)
        return leads_in_campaign
    
    def get_history(self, lead_guid, **options):
        response = self._make_request('lead/%s' % lead_guid, **options)
        leads_in_campaigns = []
        for leads in response['body']:
            leads_in_ln = CampaignLeads(leads)
            leads_in_campaigns.append(leads_in_ln)
        return leads_in_campaigns
    
    def enroll_lead(self, campaign_guid, lead_guid, **options):
        response = self._make_request('campaign/%s/add' % campaign_guid, data=str(lead_guid), method='POST', **options)
        if response['status'] == 200:
            message = "200 OK - lead enrolled"
        elif response['status'] == 401:
            message = "401 Unauthorized - bad API key"
        elif response['status'] == 404:
            message = "404 Not Found - wrong campaign or lead GUID"
        else:
            message = "400 Bad Request"
        return message
    
    def unenroll_lead(self, campaign_guid, lead_guid, **options):
        response = self._make_request('campaign/%s/remove' % campaign_guid, data=str(lead_guid), method='POST', **options)
        if response['status'] == 200:
            message = "200 OK - lead unenrolled"
        elif response['status'] == 401:
            message = "401 Unauthorized - bad API key"
        elif response['status'] == 404:
            message = "404 Not Found - wrong campaign or lead GUID"
        else:
            message = "400 Bad Request"
        return message
    

class HubSpotEventClient(HubSpotClient):
  
    def _create_path(self, subpath):
        return 'events/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, subpath)
    
    def _get_msg(self, code):
        messages = {
            200: 'successfully retrieved events',
            201: 'successfully created new event',
            401: 'unauthorized request',
            404: 'not found',
            500: 'internal server error'
        }
        return messages[code]
    
    def get_events(self, **options):
        return self._make_request('events', **options)
    
    def create_event(self, description, create_date, url, event_type, **options):
        event_data = {
            'description': description,
            'createDate': create_date,
            'url': url,
            'eventType': event_type
        }
        return self._make_request('events', data=event_data, method='POST', **options)


class HubSpotSettingsClient(HubSpotClient):
    
    def _create_path(self, subpath):
        return 'settings/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, subpath)
    
    def _get_msg(self, code):
        messages = {
            200: 'successfully retrieved settings',
            201: 'successfully updated or created new setting',
            401: 'unauthorized request',
            404: 'not found',
            500: 'internal server error'
        }
        return messages[code]
  
    def get_settings(self, **options):
        return self._make_request('settings', **options)
    
    def update_settings(self, data, **options):
        return self._make_request('settings', data=data, method='POST', **options)
  

class HubSpotBlogClient(HubSpotClient):
  
    def _create_path(self, subpath):
        return 'blog/v%s/%s' % (HUBSPOT_BLOG_API_VERSION, subpath)
    
    def _get_msg(self, code):
        messages = {
            200: 'successfully retrieved request',
            201: 'successfully updated or created resource',
            400: 'unknown error',
            404: 'not found',
            500: 'internal server error'
        }
        return messages[code]
    
    def get_blogs(self, **options):
        hs_response = self._make_request('list.json', **options)
        blog_objs = []
        for blog_json in hs_response['body']:
            individual_blog_obj = Blog(blog_json)
            blog_objs.append(individual_blog_obj)
        return blog_objs
    
    def get_blog_info(self, blog_guid, **options):
        hs_response = self._make_request(blog_guid, **options)
        individual_blog_obj = Blog(hs_response['body'])
        return individual_blog_obj
    
    def get_posts(self, blog_guid, **options):
        hs_response = self._make_request('%s/posts.json' % blog_guid, **options)
        blog_post_objs = []
        for blog_posts in hs_response['body']:
            individual_blog_obj = BlogPosts(blog_posts)
            blog_post_objs.append(individual_blog_obj)
        return blog_post_objs
    
    def get_drafts(self, blog_guid, **options):
        hs_response = self._make_request('%s/posts' % blog_guid, params={'draft': 'true'}, **options)
        blog_post_objs = []
        for blog_posts in hs_response['body']:
            individual_blog_obj = BlogPosts(blog_posts)
            blog_post_objs.append(individual_blog_obj)
        return blog_post_objs
    
    def get_published_posts(self, blog_guid, **options):
        hs_response = self._make_request('%s/posts' % blog_guid, params={'draft': 'false'}, **options)
        blog_post_objs = []
        for blog_posts in hs_response['body']:
            individual_blog_obj = BlogPosts(blog_posts)
            blog_post_objs.append(individual_blog_obj)
        return blog_post_objs
    
    def get_blog_comments(self, blog_guid, **options):
        hs_response = self._make_request('%s/comments.json' % blog_guid, **options)
        blog_comment_objs = []
        for blog_comments in hs_response['body']:
            individual_comment_obj = BlogComment(blog_comments)
            blog_comment_objs.append(individual_comment_obj)
        return blog_comment_objs
    
    def get_post(self, post_guid, **options):
        hs_response = self._make_request('posts/%s.json' % post_guid, **options)
        individual_post_obj = BlogPosts(hs_response['body'])
        return individual_post_obj
    
    def get_post_comments(self, post_guid, **options):
        hs_response = self._make_request('posts/%s/comments.json' % post_guid, **options)
        blog_comment_objs = []
        for blog_comments in hs_response['body']:
            individual_comment_obj = BlogComment(blog_comments)
            blog_comment_objs.append(individual_comment_obj)
        return blog_comment_objs
    
    def get_comment(self, comment_guid, **options):
        hs_response = self._make_request('comments/%s.json' % comment_guid, **options)
        individual_comment_obj = BlogComment(hs_response['body'])
        return individual_comment_obj
    
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
        hs_response = self._make_request('%s/posts.atom' % blog_guid, content_type='application/atom+xml', data=post, method='POST', **options)
        parsed_xml = minidom.parseString(hs_response['body'])
        inv_blog_post_obj = BlogPostCreate(parsed_xml)
        return inv_blog_post_obj
    
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
        hs_response = self._make_request('posts/%s.atom' % post_guid, content_type='application/atom+xml', data=post, method='PUT', **options)
        parsed_xml = minidom.parseString(hs_response['body'])
        inv_blog_post_obj = BlogPostCreate(parsed_xml)
        return inv_blog_post_obj
    
    def publish_post(self, post_guid, publish_time, is_draft, should_notify, **options):
        post = '''<?xml version="1.0" encoding="utf-8"?>
                <entry xmlns="http://www.w3.org/2005/Atom" xmlns:hs="http://www.hubspot.com/">
                    <published>%s</published>
                    <hs:draft>%s</hs:draft>
                    <hs:sendNotifications>%s</hs:sendNotifications>
                </entry>''' % (publish_time, is_draft, should_notify)
        hs_response = self._make_request('posts/%s.atom' % post_guid, content_type = 'application/atom+xml', data=post, method='PUT', **options)
        parsed_xml = minidom.parseString(hs_response['body'])
        inv_blog_post_obj = BlogPostCreate(parsed_xml)
        return inv_blog_post_obj
    
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
        hs_response = self._make_request('posts/%s/comments.atom' % post_guid, content_type='application/atom+xml', data=post, method='POST', **options)
        #print hs_response['body']
        parsed_xml = minidom.parseString(hs_response['body'])
        inv_blog_post_obj = BlogCommentCreate(parsed_xml)
        return inv_blog_post_obj
    

# UTILITIES
def _hs_decode(s):
    return base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4))

def verify_signed_hubspot_request(signed_request):
    """
    Return the payload from the signed request, or raise an informative
    exception if it fails to decode properly
    """
    if not signed_request:
        raise Exception("No signed request passed in")

    signed_request = str(signed_request) # convert from unicode

    if "." not in signed_request:
        raise Exception("improperly formed signed request -- missing '.'")

    signature, payload = signed_request.split(".",1)
    if not signature:
        raise Exception("No signature found in signed request")

    decoded_signature = _hs_decode(signature)
    decoded_payload = _hs_decode(payload)

    expected_signature = hmac.new(MARKETPLACE_SECRET, decoded_payload, hashlib.sha1).digest()

    if(expected_signature != decoded_signature):
        raise Exception("Signature doesn't match expectation")

    return decoded_payload
