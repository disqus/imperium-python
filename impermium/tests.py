import mock
import os.path
import unittest2

from StringIO import StringIO
from impermium import ImpermiumAPI

root = os.path.dirname(__file__)

class MockResponse(StringIO):
    def __init__(self, data, status=200, *args, **kwargs):
        StringIO.__init__(self, data, *args, **kwargs)
        self.status = status

class BindingsTest_20(unittest2.TestCase):
    def setUp(self):
        self.client = ImpermiumAPI(api_key='aaaaaaaaa', version='2.0')

    def test_check_comment(self):
        with mock.patch('httplib.HTTPConnection') as HTTPConnection:
            conn = HTTPConnection.return_value
            conn.getresponse.return_value = MockResponse(open(os.path.join(root, 'fixtures', '2.0', 'checkcomment.json')).read())

            response = self.client.checkComment('1', {
                'uid_ref': '12341234',
                'resource_url': 'http://example.com',
                'content': 'Hello world!',
            })

        self.assertTrue('eid' in response)
        self.assertEquals(response['eid'], 1)

class BindingsTest_30(unittest2.TestCase):
    def setUp(self):
        self.client = ImpermiumAPI(api_key='aaaaaaaaa', version='3.0')

    def test_train_analyst_comment(self):
        with mock.patch('httplib.HTTPConnection') as HTTPConnection:
            conn = HTTPConnection.return_value
            conn.getresponse.return_value = MockResponse(open(os.path.join(root, 'fixtures', '3.0', 'analystfeedback.json')).read())

            response = self.client.trainAnalystComment(params={
                'analyst_id': '1',
                'comment_id': '2',
                'content': 'Hello world!',
                'desired_result': {
                    "spam_classifier": {
                        "label": "notspam",
                    }
                },
                "timestamp": "20110915120908Z"
            })

        self.assertTrue('timestamp' in response)
        self.assertEquals(response['timestamp'], '20110915192214Z')
        self.assertTrue('response_id' in response)
        self.assertEquals(response['response_id'], 'clid_disqus@76@@8607@events2001.impermium.com')
