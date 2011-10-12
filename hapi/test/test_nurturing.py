import unittest2
import helper
from nose.plugins.attrib import attr
from hapi.nurturing import NurturingClient

class NurturingClientTest(unittest2.TestCase):
    def setUp(self):
        self.client = NurturingClient(**helper.get_options())
    
    def tearDown(self):
        pass
        
    @attr('api')
    def test_get_campaigns(self):
        campaigns = self.client.get_campaigns()
        print "\n\n------ current lead nurturing campaigns ------"
        print "%s\n" % '\n'.join([str(c) for c in campaigns])
        self.assertTrue(len(campaigns))


if __name__ == "__main__":
    unittest2.main()
