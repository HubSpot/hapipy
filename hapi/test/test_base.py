from collections import defaultdict
import unittest2
import simplejson as json
from StringIO import StringIO
from gzip import GzipFile

from hapi.base import BaseClient
from hapi.error import HapiError


class TestBaseClient(BaseClient):
    def _get_path(self, subpath):
        return 'unit_path/%s' % (subpath,)


class TestResult(object):
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def getheaders(self):
        return []


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
        
    def test_call(self):
        client = TestBaseClient('key', api_base='base', env='hudson')
        client.sleep_multiplier = .02
        client._create_request = lambda *args:None

        counter = dict(count=0)
        args = ('/my-api-path', {'bebop': 'rocksteady'})
        kwargs = dict(method='GET', data={}, doseq=False, number_retries=3)

        def execute_request_with_retries(a, b):
            counter['count'] += 1
            if counter['count'] < 2:
                raise HapiError(defaultdict(str), defaultdict(str)) 
            else:
                return TestResult(body='SUCCESS')
        client._execute_request_raw = execute_request_with_retries

        # This should fail once, and then succeed
        result = client._call(*args, **kwargs)
        self.assertEquals(2, counter['count'])
        self.assertEquals('SUCCESS', result)



        def execute_request_failed(a, b):
            raise HapiError(defaultdict(str), defaultdict(str)) 

        # This should fail and retry and still fail
        client._execute_request_raw = execute_request_failed
        raised_error = False
        try:
            client._call(*args, **kwargs)
        except HapiError:
            raised_error = True
        self.assertTrue(raised_error)

    def test_digest_result(self):
        """
        Test parsing returned data in various forms
        """
        plain_text = "Hello Plain Text"
        data = self.client._digest_result(plain_text, False)
        self.assertEquals(plain_text, data)

        raw_json = '{"hello": "json"}'
        data = self.client._digest_result(raw_json, False)
        # Should parse as json into dict
        self.assertEquals(data.get('hello'), 'json')

        # Write our data into a gzipped stream
        sio = StringIO()
        gzf = GzipFile(fileobj=sio, mode='wb')
        gzf.write('{"hello": "gzipped"}')
        gzf.close()

        data = self.client._digest_result(sio.getvalue(), True)
        self.assertEquals(data.get('hello'), 'gzipped')