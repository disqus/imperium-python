"""
impermium
~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.

>>> from impermium import ImpermiumAPI
>>> impermium = ImpermiumAPI(api_key=api_key)

>>> response = impermium.checkComment(event_id, {
>>>     'uid_ref': '12341234',
>>>     'resource_url': 'http://example.com',
>>>     'content': 'Hello world!',
>>> })

>>> if response['spam']['label'] == 'spam':
>>>     print "Uh oh, it's spam!"

"""
try:
    __version__ = __import__('pkg_resources') \
        .get_distribution('impermium').version
except:
    __version__ = 'unknown'

import httplib
import simplejson

class APIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return '%s: %s' % (self.code, self.message)

class ImpermiumAPI(object):
    HOST = 'api.impermium.com'
    
    def __init__(self, api_key, version='2.0'):
        self.api_key = api_key
        self.version = str(version)
    
    def request(self, http_method, type_, action, event_id=None, params={}):
        path = '/%(type)s/%(action)s/%(version)s/%(api_key)s' % dict(
            type=type_,
            action=action,
            version=self.version,
            api_key=self.api_key,
        )
        if event_id:
            path += '/%s' % (event_id,)
        conn = httplib.HTTPConnection(self.HOST)
        
        conn.request(http_method, path, simplejson.dumps(params), {
            'User-Agent': 'impermium-python/%s' % __version__,
            'Content-Type': 'application/json',
        })

        response = conn.getresponse()

        data = response.read()

        if data.startswith('{'):
            data = simplejson.loads(data)

        if response.status != 200:
            raise APIError(response.status, data)
        
        return data
    
    # Endpoints which check content
    checkSignup = lambda s, *a, **k: s.request('POST', 'account', 'signup', *a, **k)
    checkSignupAttempt = lambda s, *a, **k: s.request('POST', 'account', 'signup_attempt', *a, **k)
    checkInvite = lambda s, *a, **k: s.request('POST', 'connection', 'invite', *a, **k)
    checkInviteResponse = lambda s, *a, **k: s.request('POST', 'connection', 'invite_response', *a, **k)
    checkBlogEntry = lambda s, *a, **k: s.request('POST', 'content', 'blog_entry', *a, **k)
    checkChatMessage = lambda s, *a, **k: s.request('POST', 'content', 'chat_message', *a, **k)
    checkChatroomMessage = lambda s, *a, **k: s.request('POST', 'content', 'chatroom_message', *a, **k)
    checkComment = lambda s, *a, **k: s.request('POST', 'content', 'comment', *a, **k)
    checkForumMessage = lambda s, *a, **k: s.request('POST', 'content', 'forum_message', *a, **k)
    checkGeneric = lambda s, *a, **k: s.request('POST', 'content', 'generic', *a, **k)
    checkMessage = lambda s, *a, **k: s.request('POST', 'content', 'message', *a, **k)
    
    # Endpoints which train with content
    trainAnalyst = lambda s, *a, **k: s.request('POST', 'feedback', 'analyst', *a, **k)
    trainEnduser = lambda s, *a, **k: s.request('POST', 'feedback', 'enduser', *a, **k)

    # API 3.0 endpoints
    def trainAnalystComment(self, *args, **kwargs):
        assert self.version == '3.0'
        return self.request('POST', 'content/comment', 'analystfeedback', *args, **kwargs)

    def trainEnduserComment(self, *args, **kwargs):
        assert self.version == '3.0'
        return self.request('POST', 'content/comment', 'userfeedback', *args, **kwargs)
