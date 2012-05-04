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
    def __init__(self, result, request, err=None):
        super(HapiError,self).__init__(result and result.reason or "Unknown Reason")
        if result == None:
            self.result = EmptyResult()
        else:
            self.result = result
        self.request = request
        self.err = err

    def __str__(self):
        if self.request:
            return "\n---- request ----\n%s %s%s [timeout=%s]\n\n---- body ----\n%s\n\n---- headers ----\n%s\n\n---- result ----\n%s %s\n\n---- body ----\n%s\n\n---- headers ----\n%s\n\n---- trigger error ----\n%s\n" % (
                self.request['method'], self.request['host'], self.request['url'], self.request['timeout'],
                self.request['data'],
                self.request['headers'],
                self.result and self.result.status, self.result and self.result.reason,
                self.result and self.result.body,
                self.result and self.result.msg,
                self.err)
        else:
            return "\n---- result ----\n%s %s\n\n---- body ----\n%s\n\n---- headers ----\n%s\n\n---- trigger error ----\n%s\n" % (
                self.result and self.result.status, self.result and self.result.reason,
                self.result and self.result.body,
                self.result and self.result.msg,
                self.err)

    def __unicode__(self):
        return self.__str__()

# Create more specific error cases, to make filtering errors easier
class HapiBadRequest(HapiError):
    '''Error wrapper for most 40X results and 501 results'''

class HapiNotFound(HapiError):
    '''Error wrapper for 404 and 410 results'''

class HapiTimeout(HapiError):
    '''Wrapper for socket timeouts, sslerror, and 504'''

class HapiServerError(HapiError):
    '''Wrapper for most 500 errors'''
