"""
impermium
~~~~~~~~~

from impermium import ImpermiumAPI

impermium = ImpermiumAPI(api_key=api_key)

response = impermium.checkComment(event_id, {
    'uid_ref': '12341234',
    'resource_url': 'http://example.com',
    'content': 'Hello world!',
})

if response['spam']['label'] == 'spam':
    print "Uh oh, it's spam!"

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
    HOST = 'impermium.com'
    
    def __init__(self, api_key, version='2.0'):
        self.api_key = api_key
        self.version = version
    
    def request(self, http_method, type_, action, event_id, params={}):
        path = '/%(type)s/%(action)s/%(version)s/%(api_key)s/%(event_id)s' % dict(
            type=type_,
            action=action,
            version=self.version,
            api_key=self.api_key,
            event_id=event_id,
        )
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
    checkSignup = lambda s, x, d: s.request('POST', 'account', 'signup', x, d)
    checkSignupAttempt = lambda s, x, d: s.request('POST', 'account', 'signup_attempt', x, d)
    checkInvite = lambda s, x, d: s.request('POST', 'connection', 'invite', x, d)
    checkInviteResponse = lambda s, x, d: s.request('POST', 'connection', 'invite_response', x, d)
    checkBlogEntry = lambda s, x, d: s.request('POST', 'content', 'blog_entry', x, d)
    checkChatMessage = lambda s, x, d: s.request('POST', 'content', 'chat_message', x, d)
    checkChatroomMessage = lambda s, x, d: s.request('POST', 'content', 'chatroom_message', x, d)
    checkComment = lambda s, x, d: s.request('POST', 'content', 'comment', x, d)
    checkForumMessage = lambda s, x, d: s.request('POST', 'content', 'forum_message', x, d)
    checkGeneric = lambda s, x, d: s.request('POST', 'content', 'generic', x, d)
    checkMessage = lambda s, x, d: s.request('POST', 'content', 'message', x, d)
    
    # Endpoints which train with content
    trainAnalyst = lambda s, x, d: s.request('POST', 'feedback', 'analyst', x, d)
    trainEnduser = lambda s, x, d: s.request('POST', 'feedback', 'enduser', x, d)
