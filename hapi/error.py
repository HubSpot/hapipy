
class HapiError(ValueError):
    """Any problems get thrown as HapiError exceptions with the relevant info inside"""
    def __init__(self, result, request, err=None):
        super(HapiError,self).__init__(result and result.reason or "Unknown Reason")
        self.result = result
        self.request = request
        self.err = err

    def __str__(self):
        return "\n---- request ----\n%s %s%s [timeout=%s]\n\n---- body ----\n%s\n\n---- headers ----\n%s\n\n---- result ----\n%s %s\n\n---- body ----\n%s\n\n---- headers ----\n%s\n\n---- trigger error ----\n%s\n" % (
            self.request['method'], self.request['host'], self.request['url'], self.request['timeout'],
            self.request['data'],
            self.request['headers'],
            self.result and self.result.status, self.result and self.result.reason,
            self.result and self.result.body,
            self.result and self.result.msg,
            self.err)

    def __unicode__(self):
        return self.__str__()
