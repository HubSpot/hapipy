import urllib
import httplib
import simplejson as json
from error import HapiError

#class Request(object):
    #def __init__(self, method, url, data, headers)

        #super(BaseClient, self).__init__()


class BaseClient(object):
    '''Base abstract object for interacting with the HubSpot APIs'''

    def __init__(self, api_key, timeout=10, **extra_options):
        super(BaseClient, self).__init__()
        self.api_key = api_key
        self.options = {'timeout':timeout, 'api_base':'hubapi.com'}
        self.options.update(extra_options)
        self._prepare_connection_type()

    def _prepare_connection_type(self):
        connection_types = {'http': httplib.HTTPConnection, 'https': httplib.HTTPConnection}
        parts = self.options['api_base'].split('://')
        protocol = (parts[0:-1]+['https'])[0]
        self.options['connection_type'] = connection_types[protocol]
        self.options['protocol'] = protocol
        self.options['api_base'] = parts[-1]

    def _get_path(self, subpath):
        raise Exception("Unimplemented get_path for BaseClient subclass!")

    def _prepare_request(self, subpath, params, data, opts):
        params = params or {}
        params['hapikey'] = self.api_key
        if opts.get('hub_id') or opts.get('portal_id'):
            params['portalId'] = opts.get('hub_id') or opts.get('portal_id')
        url = opts.get('url') or '/%s?%s' % (self._get_path(subpath), urllib.urlencode(params))
        headers = {'Content-Type': opts.get('content_type') or 'application/json'}
        if data and not isinstance(data, str) and headers['Content-Type']=='application/json':
            data = json.dumps(data)

        return url, headers, data

    def _create_request(self, conn, method, url, headers, data):
        conn.request(method, url, data, headers)
        return {'method':method, 'url':url, 'data':data, 'headers':headers, 'host':conn.host, 'timeout':conn.timeout}

    def _execute_request(self, conn, request):
        result = conn.getresponse()
        result.body = result.read()
        
        data = result.body
        conn.close()
        if result.status >= 400:
            raise HapiError(result, request)

        return data

    def _digest_result(self, data):
        if data and isinstance(data, str):
            try:
                data = json.loads(data)
            except ValueError:  
                pass

        return data

    def _call(self, subpath, params=None, method='GET', data=None, **options):
        opts = self.options.copy()
        opts.update(options)

        url, headers, data = self._prepare_request(subpath, params, data, opts)

        connection = opts['connection_type'](opts['api_base'], timeout=opts['timeout'])
        request_info = self._create_request(connection, method, url, headers, data)

        data = self._execute_request(connection, request_info)
        return self._digest_result(data)

    def mixin(self, mixin_class):
        if mixin_class not in self.__class__.__bases__:
            self.__class__.__bases__ = (mixin_class,) + self.__class__.__bases__

    
