
class HapiError(ValueError):
    """Any problems get thrown as HapiError exceptions with the relevant info inside"""
    def __init__(self, result):
        super(HapiError,self).__init__()
        self.result = result
        self.reason = result.reason
        self.status = result.status
        self.msg = result.msg
        self.body = result.body
