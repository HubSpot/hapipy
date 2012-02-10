'''
The the mixins in this file require PyCURL in order to make parallel API calls.  
On OSX and Linux machines, PyCURL can be installed via pip (run "pip install pycurl" ).  
For windows machines, pre-compiled PyCURL binaries can be downloaded 
[here for python 2.6 and 2.7](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl), and 
[here for python 2.5](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pycurl).
'''

import pycurl, cStringIO

class HapiThreadedError(ValueError):
    def __init__(self, curl):
        super(HapiThreadedError, self).__init__(curl.body.getvalue())
        self.c = curl
        self.response_body = self.c.body.getvalue()
        self.response_headers = self.c.response_headers.getvalue()

    def __str__(self):
        return "\n---- request ----\n%s %s%s [timeout=%s]\n\n---- body ----\n%s\n\n---- headers ----\n%s\n\n---- result ----\n%s\n\n---- body ----\n%s\n\n---- headers ----\n%s" % (
            getattr(self.c, 'method', ''), 
            self.c.host, 
            self.c.path, 
            self.c.timeout,
            self.c.data,
            self.c.headers,
            self.c.status,
            self.response_body,
            self.response_headers)

    def __unicode__(self):
        return self.__str__()

class PyCurlMixin(object):
    """
    PyCurlMixin relies on PyCurl, which is a library around libcurl which enables efficient
    multi-threaded requests.  Use this mixin when you want to be able to execute multiple
    API calls at once, instead of in sequence.

    Enable by calling client.mixin(PyCurlMixin) after importing PyCurlMixin and instantiating
    the client of your choice.

    Once enabled, use like so:
        client.my_api_call()
        client.my_other_api_call()
        results = client.process_queue()

    The results object will then return a list of dicts, containing the response to your calls
    in the order they were called. Dicts have keys: data, code, and (if something went wrong) exception.
    """
    def _call(self, subpath, params=None, method='GET', data=None, doseq=False, **options):
        opts = self.options.copy()
        opts.update(options)

        request_parts = self._prepare_request(subpath, params, data, opts, doseq=doseq)
        self._enqueue(request_parts)

    def _enqueue(self, parts):
        if not hasattr(self, "_queue"):
            self._queue = []

        self._queue.append(parts)

    def _create_curl(self, url, headers, data):
        c = pycurl.Curl()

        full_url = "%s://%s%s" % (self.options['protocol'], self.options['api_base'], url)
        
        c.timeout = self.options['timeout']
        c.protocol = self.options['protocol']
        c.host = self.options['api_base']
        c.path = url
        c.full_url = full_url
        c.headers = headers
        c.data = data

        c.status = -1
        c.body = cStringIO.StringIO()
        c.response_headers = cStringIO.StringIO()

        c.setopt(c.URL, c.full_url)
        c.setopt(c.TIMEOUT, self.options['timeout'])
        c.setopt(c.WRITEFUNCTION, c.body.write)
        c.setopt(c.HEADERFUNCTION, c.response_headers.write)

        if headers:
            c.setopt(c.HTTPHEADER, [ "%s: %s" % (x, y) for x, y in headers.items() ])

        if data:
            c.data_out = cStringIO.StringIO(data)
            c.setopt(c.READFUNCTION, c.data_out.getvalue)

        return c

    def process_queue(self):
        """
        Processes all API calls since last invocation, returning a list of data
        in the order the API calls were created
        """
        m = pycurl.CurlMulti()
        m.handles = []

        # Loop the queue and create Curl objects for processing
        for item in self._queue:
            c = self._create_curl(*item)
            m.add_handle(c)
            m.handles.append(c)

        # Process the collected Curl handles
        num_handles = len(m.handles)
        while num_handles:
            while 1:
                # Perform the calls
                ret, num_handles = m.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break
            m.select(1.0)

        # Collect data
        results = []
        for c in m.handles:
            c.status = c.getinfo(c.HTTP_CODE)
            result = { "data" : self._digest_result(c.body.getvalue()), "code": c.status }
            if not c.status or c.status >= 400:
                # Don't throw the exception because some might have succeeded
                result['exception'] = HapiThreadedError(c)

            results.append(result)

            
        # cleanup
        for c in m.handles:
            if hasattr(c, "data_out"):
                c.data_out.close()

            c.body.close()
            c.response_headers.close()
            c.close()
            m.remove_handle(c)

        m.close()
        del m.handles
        self._queue = []

        return results 
