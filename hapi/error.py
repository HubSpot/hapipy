
class HapiError(ValueError):
    """Any problems get thrown as HapiError exceptions with the relevant info inside"""
    def __init__(self, result, request):
        super(HapiError,self).__init__(result.reason)
        self.result = result
        self.request = request

    def __str__(self):
        return "\n---- request ----\n%s %s%s [timeout=%s]\n\n---- body ----\n%s\n\n---- headers ----\n%s\n\n---- result ----\n%s %s\n\n---- body ----\n%s\n\n---- headers ----\n%s" % (
            self.request['method'], self.request['host'], self.request['url'], self.request['timeout'],
            self.request['data'],
            self.request['headers'],
            self.result.status, self.result.reason,
            self.result.body,
            self.result.msg)

    def __unicode__(self):
        return self.__str__()
