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
        self.options['api_base'] = parts[-1]

    def _get_path(self, subpath):
        raise Exception("Unimplemented get_path for BaseClient subclass!")

    def _create_request(self, conn, subpath, params, method, data, opts):
        params = params or {}
        params['hapikey'] = self.api_key
        if opts.get('hub_id') or opts.get('portal_id'):
            params['portalId'] = opts.get('hub_id') or opts.get('portal_id')
        url = opts.get('url') or '/%s?%s' % (self._get_path(subpath), urllib.urlencode(params))
        headers = {'Content-Type': opts.get('content_type') or 'application/json'}
        if not isinstance(data, str) and headers['Content-Type']=='application/json':
            data = json.dumps(data)
        #logger.debug("%s %s%s  %s %s", (method, opts['api_base'], url, data, headers))
        conn.request(method, url, data, headers)
        return {'method':method, 'url':url, 'data':data, 'headers':headers, 'host':conn.host, 'timeout':conn.timeout}

    def _digest_result(self, conn, request):
        result = conn.getresponse()
        result.body = result.read()
        #logger.debug("%s %s\n---message---\n%s\n---body---\n%s\n---headers---\n%s\n",
                #(result.status, result.reason, result.msg, result_read, result.getheaders()))
        data = result.body
        conn.close()
        if result.status >= 400:
            raise HapiError(result, request)
        if data and isinstance(data, str):
            try:
                data = json.loads(data)
            except ValueError:  
                pass
        return data

    def _call(self, subpath, params=None, method='GET', data=None, **options):
        opts = self.options.copy()
        opts.update(options)

        connection = opts['connection_type'](opts['api_base'], timeout=opts['timeout'])
        request_info = self._create_request(connection, subpath, params, method, data, opts)
        return self._digest_result(connection, request_info)

    
