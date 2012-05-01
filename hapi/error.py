
class HapiError(ValueError):
    """Any problems get thrown as HapiError exceptions with the relevant info inside"""
    def __init__(self, result, request, err=None):
        super(HapiError,self).__init__(result and result.reason or "Unknown Reason")
        self.result = result
        self.request = request
        self.err = err

    def __str__(self):
        error_string = ''
        error_data = {}

        if self.request:
            error_string += "\n---- request ----\n%(method)s %(host)s%(url)s [timeout=%(timeout)s]\n\n---- body ----\n%(data)s\n\n---- headers ----\n%(headers)s\n"

            error_data['method'] = self.request['method']
            error_data['host'] = self.request['host']
            error_data['url'] = self.request['url']
            error_data['timeout'] = self.request['timeout']
            error_data['data'] = self.request['data']
            error_data['headers'] = self.request['headers']

        if self.result:
            error_string += "\n---- result ----\n%(status)s %(reason)s\n\n---- body ----\n%(body)s\n\n---- headers ----\n%(msg)s\n"

            error_data['status'] = self.result and self.result.status
            error_data['reason'] = self.result and self.result.reason
            error_data['body'] = self.result and self.result.body
            error_data['msg'] = self.result and self.result.msg

        if self.err:
            error_string += "\n---- trigger error ----\n%(err)s\n"

            error_data['err'] = self.err

        return error_string % error_data

    def __unicode__(self):
        return self.__str__()
