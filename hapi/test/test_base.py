import unittest2

from hapi.base import BaseClient


class TestBaseClient(BaseClient):
    def _get_path(self, subpath):
        return 'unit_path/%s' % (subpath,)


class BaseTest(unittest2.TestCase):

    def setUp(self):
        self.client = TestBaseClient('unit_api_key')

    def tearDown(self):
        pass

    def test_prepare_request(self):
        subpath = 'unit_sub_path'
        params = {'duplicate': ['key', 'value']}
        data = None
        opts = {}
        doseq = False

        # with doseq=False we should encode the array
        # so duplicate=[key,value]
        url, headers, data = self.client._prepare_request(subpath, params, data, opts, doseq)
        self.assertTrue('duplicate=%5B%27key%27%2C+%27value%27%5D' in url)

        # with doseq=True the values will be split and assigned their own key
        # so duplicate=key&duplicate=value
        doseq = True
        url, headers, data = self.client._prepare_request(subpath, params, data, opts, doseq)
        print url
        self.assertTrue('duplicate=key&duplicate=' in url)
