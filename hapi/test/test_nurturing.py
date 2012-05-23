import unittest2
import helper
from nose.plugins.attrib import attr
from hapi.nurturing import NurturingClient
from hapi.mixins.threading import PyCurlMixin

class NurturingClientTest(unittest2.TestCase):
    def setUp(self):
        self.client = NurturingClient(**helper.get_options())
    
    def tearDown(self):
        pass
        
    @attr('api')
    def test_get_campaigns(self):
        campaigns = self.client.get_campaigns()
        self._check_result(campaigns)
        
    def test_parallel_get_campaigns(self):
        # Because the client established in setup does not have PyCurlMixin,
        # make another client to handle parallel get campaigns.
        # All the options are the same, except mixins is PyCurlMixin
        opts = helper.get_options()
        
        opts['mixins'] = [PyCurlMixin]

        self.parallel_client = NurturingClient(**opts)
        
        self.parallel_client.get_campaigns()
        self.parallel_client.get_campaigns()

        results = self.parallel_client.process_queue()
        for result in results:
            self.assertTrue('data' in result)
            self.assertTrue('code' in result)
            self._check_result(result['data'])

    def _check_result(self, campaigns):
        print "\n\n------ current lead nurturing campaigns ------"
        print "%s\n" % '\n'.join([str(c) for c in campaigns])
        self.assertTrue(len(campaigns))

if __name__ == "__main__":
    unittest2.main()
