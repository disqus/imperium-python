import mock
import unittest2

from StringIO import StringIO
from impermium import ImpermiumAPI

class MockResponse(StringIO):
    def __init__(self, data, status=200, *args, **kwargs):
        StringIO.__init__(self, data, *args, **kwargs)
        self.status = status

class MockImpermiumAPI(ImpermiumAPI):
    def request(self, http_method, type_, action, event_id=None, params={}):
        with mock.patch('httplib.HTTPConnection') as HTTPConnection:
            conn = HTTPConnection.return_value
            conn.getresponse.return_value = MockResponse(("""
            {
                "rid" : 79898989,
                "eid" : %(event_id)s,
                "etype" : 20,
                "ts" : "20110208123409Z",
                "spam" : {
                    "label" : "notspam",
                    "confidence" : "high",
                    "confidence_score" : 0.97,
                    "reason" : "" 
                },
                "porn" : {
                    "label" : "porn",
                    "confidence" : "high",
                    "confidence_score" : 0.89,
                    "reason" : "adult content",
                    "urls" : [
                        "www.dirtynasty.com",
                        "xxx.org" 
                    ] 
                },
                "profanity" : {
                    "label" : "profane",
                    "confidence_score" : "0.6",
                    "confidence" : "medium",
                    "reason" : "2+ block words",
                    "block_words_found" : [
                        "bi***",
                        "f***" 
                    ] 
                },
                "quality" : {
                    "iq_score": 0.99,
                    "label" : "low_quality",
                    "confidence" : "high",
                    "confidence_score" : "0.9" 
                } 
            }""" % dict(
                event_id=event_id,
            )).strip())
            return super(MockImpermiumAPI, self).request(http_method, type_, action, event_id=event_id, params=params)

class BindingsTest_20(unittest2.TestCase):
    def setUp(self):
        self.client = MockImpermiumAPI(api_key='aaaaaaaaa', version='2.0')

    def test_check_comment(self):
        response = self.client.checkComment('1', {
            'uid_ref': '12341234',
            'resource_url': 'http://example.com',
            'content': 'Hello world!',
        })
        self.assertTrue('eid' in response)
        self.assertEquals(response['eid'], 1)
