class EmptyResult(object):
    '''
    Null Object pattern to prevent Null reference errors 
    when there is no result
    '''
    def __init__(self):
        self.status = 0
        self.body = ''
        self.msg = ''
        self.reason = ''

    def __nonzero__(self):
        return False


class HapiError(ValueError):
    """Any problems get thrown as HapiError exceptions with the relevant info inside"""

    as_str_template = u'''
---- request ----
{method} {host}{url}, [timeout={timeout}]

---- body ----
{body}

---- headers ----
{headers}

---- result ----
{result_status}

---- body -----
{result_body}

---- headers -----
{result_headers}

---- reason ----
{result_reason}

---- trigger error ----
{error}
        '''


    def __init__(self, result, request, err=None):
        super(HapiError,self).__init__(result and result.reason or "Unknown Reason")
        if result == None:
            self.result = EmptyResult()
        else:
            self.result = result
        if request == None:
            request = {}
        self.request = request
        self.err = err

    def __str__(self):
        return self.__unicode__().encode('ascii', 'replace')


    def __unicode__(self):
        params = {}
        request_keys = ('method', 'host', 'url', 'data', 'headers', 'timeout', 'body')
        result_attrs = ('status', 'reason', 'msg', 'body', 'headers')
        params['error'] = self.err
        for key in request_keys:
            params[key] = self.request.get(key)
        for attr in result_attrs:
            params['result_%s' % attr] = getattr(self.result, attr, '')
        
        params = self._dict_vals_to_unicode(params)
        return self.as_str_template.format(**params)

    def _dict_vals_to_unicode(self, data):
        unicode_data = {}
        for key, val in data.items():
            if not isinstance(val, basestring):
                unicode_data[key] = unicode(val)
            elif not isinstance(val, unicode):
                unicode_data[key] = unicode(val, 'utf8', 'ignore')
            else:
                unicode_data[key] = val
        return unicode_data



# Create more specific error cases, to make filtering errors easier
class HapiBadRequest(HapiError):
    '''Error wrapper for most 40X results and 501 results'''

class HapiNotFound(HapiError):
    '''Error wrapper for 404 and 410 results'''

class HapiTimeout(HapiError):
    '''Wrapper for socket timeouts, sslerror, and 504'''

class HapiServerError(HapiError):
    '''Wrapper for most 500 errors'''
