import urllib
import httplib
import simplejson as json
import utils
import logging
import sys
import time
import traceback
import gzip
import StringIO

from error import HapiError, HapiBadRequest, HapiNotFound, HapiTimeout, HapiServerError, HapiUnauthorized


_PYTHON25 = sys.version_info < (2, 6)

class BaseClient(object):
    '''Base abstract object for interacting with the HubSpot APIs'''

    # Controls how long we sleep for during retries, overridden by unittests
    # so tests run faster
    sleep_multiplier = 1

    def __init__(self, api_key=None, timeout=10, mixins=[], access_token=None, refresh_token=None, client_id=None,  **extra_options):
        super(BaseClient, self).__init__()
        # reverse so that the first one in the list because the first parent
        mixins.reverse()
        for mixin_class in mixins:
            if mixin_class not in self.__class__.__bases__:
                self.__class__.__bases__ = (mixin_class,) + self.__class__.__bases__

        self.api_key = api_key or extra_options.get('api_key')
        self.access_token = access_token or extra_options.get('access_token')
        self.refresh_token = refresh_token or extra_options.get('refresh_token')
        self.client_id = client_id or extra_options.get('client_id')
        self.log = utils.get_log('hapipy')
        if self.api_key and self.access_token:
            raise Exception("Cannot use both api_key and access_token.")
        if not (self.api_key or self.access_token or self.refresh_token):
            raise Exception("Missing required credentials.")
        self.options = {'api_base': 'api.hubapi.com'}
        if not _PYTHON25:
            self.options['timeout'] = timeout
        self.options.update(extra_options)
        self._prepare_connection_type()

    def _prepare_connection_type(self):
        connection_types = {'http': httplib.HTTPConnection, 'https': httplib.HTTPSConnection}
        parts = self.options['api_base'].split('://')
        protocol = (parts[0:-1]+['https'])[0]
        self.options['connection_type'] = connection_types[protocol]
        self.options['protocol'] = protocol
        self.options['api_base'] = parts[-1]

    def _get_path(self, subpath):
        raise Exception("Unimplemented get_path for BaseClient subclass!")

    def _prepare_request(self, subpath, params, data, opts, doseq=False, query=''):
        params = params or {}
        if self.api_key:
            params['hapikey'] = params.get('hapikey') or self.api_key
        else:
            # Be sure that we're consistent about what access_token is being used
            # If one was provided at instantiation, that is always used.  If it was not
            # but one was provided as part of the method invocation, we persist it
            if params.get('access_token') and not self.access_token:
                self.access_token = params.get('access_token')
            params['access_token'] = self.access_token

        if opts.get('hub_id') or opts.get('portal_id'):
            params['portalId'] = opts.get('hub_id') or opts.get('portal_id')
        if query == None:
            query = ''
        if query and query.startswith('?'):
            query = query[1:]
        if query and not query.startswith('&'):
            query = '&' + query
        url = opts.get('url') or '/%s?%s%s' % (self._get_path(subpath), urllib.urlencode(params, doseq), query)
        headers = opts.get('headers') or {}
        headers.update({
            'Accept-Encoding': 'gzip',
            'Content-Type': opts.get('content_type') or 'application/json'})

        if data and not isinstance(data, basestring) and headers['Content-Type']=='application/json':
            data = json.dumps(data)

        return url, headers, data

    def _create_request(self, conn, method, url, headers, data):
        conn.request(method, url, data, headers)
        params = {'method':method, 'url':url, 'data':data, 'headers':headers, 'host':conn.host}
        if not _PYTHON25:
            params['timeout'] = conn.timeout
        return params

    def _gunzip_body(self, body):
        sio = StringIO.StringIO(body)
        gf = gzip.GzipFile(fileobj=sio, mode="rb")
        return gf.read()

    def _process_body(self, data, gzipped):
        if gzipped:
            return self._gunzip_body(data)
        return data

    def _execute_request_raw(self, conn, request):
        try:
            result = conn.getresponse()
        except:
            raise HapiTimeout(None, request, traceback.format_exc())

        encoding = [i[1] for i in result.getheaders() if i[0] == 'content-encoding']
        result.body = self._process_body(result.read(), len(encoding) and encoding[0] == 'gzip')

        conn.close()
        if result.status in (404, 410):
            raise HapiNotFound(result, request)
        elif result.status == 401:
            raise HapiUnauthorized(result, request)
        elif result.status >= 400 and result.status < 500 or result.status == 501:
            raise HapiBadRequest(result, request)
        elif result.status >= 500:
            raise HapiServerError(result, request)

        return result

    def _execute_request(self, conn, request):
        result = self._execute_request_raw(conn, request)
        return result.body

    def _digest_result(self, data):
        if data and isinstance(data, basestring):
            try:
                data = json.loads(data)
            except ValueError:
                pass

        return data

    def _call_raw(self, subpath, params=None, method='GET', data=None, doseq=False, query='', retried=False, **options):
        opts = self.options.copy()
        opts.update(options)
        url, headers, data = self._prepare_request(subpath, params, data, opts, doseq, query)
        kwargs = {}
        if not _PYTHON25:
            kwargs['timeout'] = opts['timeout']

        num_retries = opts.get('number_retries', 0)
        # Never retry a POST, PUT, or DELETE unless explicitly told to
        if method != 'GET' and not opts.get('retry_on_post'):
            num_retries = 0
        if num_retries > 6:
            num_retries = 6
        emergency_brake = 10
        try_count = 0
        while True:
            emergency_brake -= 1
            # avoid getting burned by any mistakes in While loop logic
            if emergency_brake < 1:
                break
            try:
                try_count += 1
                connection = opts['connection_type'](opts['api_base'], **kwargs)
                request_info = self._create_request(connection, method, url, headers, data)
                result = self._execute_request_raw(connection, request_info)
                break
            except HapiUnauthorized, e:
                self.log.warning("401 Unauthorized response to API request.")
                if self.access_token and self.refresh_token and self.client_id and not retried:
                    self.log.info("Refreshing access token")
                    try:
                        token_response = utils.refresh_access_token(self.refresh_token, self.client_id)
                        decoded = json.loads(token_response)
                        self.access_token = decoded['access_token']
                        self.log.info('Retrying with new token %' % (self.access_token))
                    except Exception, e:
                        self.log.error("Unable to refresh access_token: %s" % (e))
                        raise
                    return self._call_raw(subpath, params=params, method=method, data=data, doseq=doseq, query=query, retried=True, **options)
                else:
                    if self.access_token and self.refresh_token and self.client_id and retried:
                        self.log.error("Refreshed token, but request still was not authorized.  You may need to grant additional permissions.")
                    elif self.access_token and not self.refresh_token:
                        self.log.error("In order to enable automated refreshing of your access token, please provide a refresh token as well.")
                    elif self.access_token and not self.client_id:
                        self.log.error("In order to enable automated refreshing of your access token, please provide a client_id in addition to a refresh token.")
                    raise
            except HapiError, e:
                if try_count > num_retries:
                    logging.warning("Too many retries for %s", url)
                    raise
                # Don't retry errors from 300 to 499
                if e.result and e.result.status >= 300 and e.result.status < 500:
                    raise
                self.log.warning('HapiError %s calling %s, retrying' % (e, url))
            # exponential back off - wait 0 seconds, 1 second, 3 seconds, 7 seconds, 15 seconds, etc.
            time.sleep((pow(2, try_count - 1) - 1) * self.sleep_multiplier)
        return result

    def _call(self, subpath, params=None, method='GET', data=None, doseq=False, query='', **options):
        result = self._call_raw(subpath, params=params, method=method, data=data, doseq=doseq, query=query, retried=False, **options)
        return self._digest_result(result.body)
