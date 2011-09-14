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
__author__ = "Adrian Mott"
__author__ = "Matt Furtado"

import re
import hmac
import base64
import urllib
import httplib
import logging
from xml.dom import minidom
from blog_objects import *

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
try:
  from hubspot.settings import settings as hs_settings
  HUBSPOT_API_BASE = hs_settings.HUBSPOT_API_BASE
except:
  HUBSPOT_API_BASE = "hubapi.com"

HUBSPOT_BLOG_API_VERSION = '1'
HUBSPOT_LEADS_API_VERSION = '1'


class HubSpotClient(object):
  '''Client for interacting with the HubSpot APIs'''
  
  def __init__(self, api_key):
    self.api_key = api_key
    self.portal_id = None
  
  def _create_path(self, method):
    pass
  
  def _http_error(self, code, message, url):
    logging.error('Client request error. Code: %s - Reason: %s - URL: %s' % (str(code), message, url))
  
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
  
  def _deal_with_content_type(self, output):
    if output == "atom" or output == "xml":
      return "atom+xml"
    return "json"
  
  def _make_request(self, method, params, content_type, data=None, request_method='GET', url=None):
    params['hapikey'] = self.api_key
    
    if self.portal_id:
      params['portalId'] = self.portal_id
    
    if not url: url = '/%s?%s' % (self._create_path(method), urllib.urlencode(params))
    
    client = httplib.HTTPSConnection(HUBSPOT_API_BASE)
    if data and not isinstance(data, str):
      data = urllib.urlencode(data)
    
    headers = {'Content-Type': content_type}
    
    client.request(request_method, url, data, headers)
    
    result = client.getresponse()
    if result.status < 400:
      body = result.read()
      client.close()
      if body:
        return self._prepare_response(result.status, body)
      else:
        return self._prepare_response(result.status, None)
    else:
      client.close()
      self._http_error(result.status, result.reason, url)
      return self._prepare_response(result.status, {})
  
class HubSpotLeadsClient(HubSpotClient):
  """
    The PySpot Leads client uses the _make_request method to call the API for data.  It returns only JSON in the standard format:
    { status: 'status', body: 'data from API call', msg: 'message' }
    PLEASE NOTE that the 'body' here is decoded JSON.
  """
  def _create_path(self, method):
    return 'leads/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, method)
  
  def create_lead(self, ip_address, cookie, fields):
    pass
    
  def get_lead(self, lead_guid):
    return self._make_request('list/', {'guids[0]': lead_guid})
  
  def search_leads(self, term, params):
    params['search'] = term
    return self._make_request('list/', params)
    
  def update_lead(self, lead_guid, data):
    return self._make_request(
      'lead/%s/' % lead_guid, {},
      data=data, request_method='PUT'
    )
  
  def get_callback_urls(self):
    return self._make_request(
      'callback-url', {}
    )
    
  def register_callback_url(self, url):
    return self._make_request(
      'callback-url', {'url': url}, data={'url': url}, request_method='POST'
    )
    
  def close_lead(self, lead_guid):
    now = int(time.time()*1000)
    data = {'closedAt': now}
    return self._make_request(
      'lead/%s/' % lead_guid, data, request_method='PUT'
    )
    

class HubSpotLeadNurtureClient(HubSpotClient):
  
  def _create_path(self, method):
    return 'nurture/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, method)
    
  def get_campaigns(self):
    return self._make_request(
      'campaigns', {}
    )
    
  def get_leads(self, campaign_guid):
    return self._make_request(
      'campaign/%s/list' % campaign_guid, {}
    )
  
  def get_history(self, lead_guid):
    return self._make_request(
      'lead/%s' % lead_guid, {}
    )
    
  def enroll_lead(self, campaign_guid):
    return self._make_request(
      'campaign/%s/add' % campaign_guid, {}
    )
    
  def unenroll_lead(self, campaign_guid):
    return self._make_request(
      'campaign/%s/remove' % campaign_guid, {}
    )


class HubSpotEventClient(HubSpotClient):
  
  def _create_path(self, method):
    return 'events/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, method)
    
  def _get_msg(self, code):
    messages = {
      200: 'successfully retrieved events',
      201: 'successfully created new event',
      401: 'unauthorized request',
      404: 'not found',
      500: 'internal server error'
    }
    return messages[code]
    
  def get_events(self):
    return self._make_request(
      'events', {}
    )
    
  def create_event(self, description, create_date, url, event_type):
    event_data = {
      'description': description,
      'createDate': create_date,
      'url': url,
      'eventType': event_type
    }
    return self._make_request(
      'events', {}, data=event_data, request_method='POST'
    )


class HubSpotSettingsClient(HubSpotClient):
  
  def _create_path(self, method):
    return 'settings/v%s/%s' % (HUBSPOT_LEADS_API_VERSION, method)
    
  def _get_msg(self, code):
    messages = {
      200: 'successfully retrieved settings',
      201: 'successfully updated or created new setting',
      401: 'unauthorized request',
      404: 'not found',
      500: 'internal server error'
    }
    return messages[code]
    
  def get_settings(self):
    return self._make_request(
      'settings', {}
    )    
    
  def update_settings(self, data):
    return self._make_request(
      'settings', {}, request_method='POST', data=data
    )
    
class HubSpotBlogClient(HubSpotClient):
  
  def _create_path(self, method):
    return 'blog/v%s/%s' % (HUBSPOT_BLOG_API_VERSION, method)

  def _get_msg(self, code):
    messages = {
      200: 'successfully retrieved request',
      201: 'successfully updated or created resource',
      400: 'unknown error',
      404: 'not found',
      500: 'internal server error'
    }
    return messages[code]
  
  def get_blogs(self):
    hs_response = self._make_request('list.json', {}, 'application/json')
    blog_objs = []
    for blog_json in hs_response['body']:
      individual_blog_obj = Blog(blog_json)
      blog_objs.append(individual_blog_obj)
    return blog_objs
  
  def get_blog_info(self, blog_guid):
    hs_response = self._make_request(blog_guid, {}, 'application/json')
    individual_blog_obj = Blog(hs_response['body'])
    return individual_blog_obj
  
  def get_posts(self, blog_guid):
    hs_response = self._make_request('%s/posts.json' % blog_guid, {}, 'application/json')
    blog_post_objs = []
    for blog_posts in hs_response['body']:
      individual_blog_obj = BlogPosts(blog_posts)
      blog_post_objs.append(individual_blog_obj)
    return blog_post_objs
  
  def get_drafts(self, blog_guid):
    hs_response = self._make_request('%s/posts' % blog_guid, {'draft': 'true'}, 'application/json')
    blog_post_objs = []
    for blog_posts in hs_response['body']:
      individual_blog_obj = BlogPosts(blog_posts)
      blog_post_objs.append(individual_blog_obj)
    return blog_post_objs
  
  def get_published_posts(self, blog_guid):
    hs_response = self._make_request('%s/posts' % blog_guid, {'draft': 'false'}, 'application/json')
    blog_post_objs = []
    for blog_posts in hs_response['body']:
      individual_blog_obj = BlogPosts(blog_posts)
      blog_post_objs.append(individual_blog_obj)
    return blog_post_objs
  
  def get_blog_comments(self, blog_guid):
    hs_response = self._make_request('%s/comments.json' % blog_guid, {}, 'application/json')
    blog_comment_objs = []
    for blog_comments in hs_response['body']:
      individual_comment_obj = BlogComment(blog_comments)
      blog_comment_objs.append(individual_comment_obj)
    return blog_comment_objs
  
  def get_post(self, post_guid):
    hs_response = self._make_request('posts/%s.json' % post_guid, {}, 'application/json')
    individual_post_obj = BlogPosts(hs_response['body'])
    return individual_post_obj
    
  def get_post_comments(self, post_guid):
    hs_response = self._make_request('posts/%s/comments.json' % post_guid, {}, 'application/json')
    blog_comment_objs = []
    for blog_comments in hs_response['body']:
      individual_comment_obj = BlogComment(blog_comments)
      blog_comment_objs.append(individual_comment_obj)
    return blog_comment_objs
      
  def get_comment(self, comment_guid):
    hs_response = self._make_request('comments/%s.json' % comment_guid, {}, 'application/json')
    individual_comment_obj = BlogComment(hs_response['body'])
    return individual_comment_obj
    
  def create_post(self, blog_guid, author_name, author_email, title, summary, content, tags):
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
    hs_response = self._make_request('%s/posts.atom' % blog_guid, {}, content_type='application/atom+xml', data=post, request_method='POST')
    parsed_xml = minidom.parseString(hs_response['body'])
    inv_blog_post_obj = BlogPostCreate(parsed_xml)
    return inv_blog_post_obj
  
  def update_post(self, post_guid, title, summary, content, meta_desc, meta_keyword, tags):
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
    hs_response = self._make_request('posts/%s.atom' % post_guid, {}, content_type='application/atom+xml', data=post, request_method='PUT')
    parsed_xml = minidom.parseString(hs_response['body'])
    inv_blog_post_obj = BlogPostCreate(parsed_xml)
    return inv_blog_post_obj
  
  def publish_post(self, post_guid, publish_time, is_draft, should_notify):
    post = '''<?xml version="1.0" encoding="utf-8"?>
              <entry xmlns="http://www.w3.org/2005/Atom" xmlns:hs="http://www.hubspot.com/">
                <published>%s</published>
                <hs:draft>%s</hs:draft>
                <hs:sendNotifications>%s</hs:sendNotifications>
              </entry>''' % (publish_time, is_draft, should_notify)
    hs_response = self._make_request('posts/%s.atom' % post_guid, {}, content_type = 'application/atom+xml', data=post, request_method='PUT')
    parsed_xml = minidom.parseString(hs_response['body'])
    inv_blog_post_obj = BlogPostCreate(parsed_xml)
    return inv_blog_post_obj
    
  def create_comment(self, post_guid, author_name, author_email, author_uri, content):
    post = '''<?xml version="1.0" encoding="utf-8"?>
              <entry xmlns="http://www.w3.org/2005/Atom">
                <author>
                  <name>%s</name>
                  <email>%s</email>
                  <uri>%s</uri>
                </author>
                <content type="html"><![CDATA[%s]]></content>
              </entry>''' % (author_name, author_email, author_uri, content)
    hs_response = self._make_request('posts/%s/comments.atom' % post_guid, {}, content_type='application/atom+xml', data=post, request_method='POST')
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
