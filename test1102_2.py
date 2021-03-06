#!/usr/bin/python
# coding: utf-8

import facebook
import urllib
import urlparse
import subprocess
import warnings

# Keep Facebook settings like APP_ID
#import settings
FACEBOOK_APP_ID     = '1085103088207726'
FACEBOOK_APP_SECRET = 'ca9098b03e1cc79c26b46013e3854444'
FACEBOOK_PROFILE_ID = '100001752101318'


# Hide deprecation warnings. The facebook module isn't that up-to-date (facebook.GraphAPIError).
warnings.filterwarnings('ignore', category=DeprecationWarning)


# Trying to get an access token. Very awkward.
oauth_args = dict(client_id     = FACEBOOK_APP_ID, #settings.FACEBOOK_APP_ID,
                  client_secret = FACEBOOK_APP_SECRET, #settings.FACEBOOK_APP_SECRET,
                  grant_type    = 'client_credentials')
oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]

try:
    oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
except KeyError:
    print('Unable to grab an access token!')
    exit()

facebook_graph = facebook.GraphAPI(oauth_access_token)


# Try to post something on the wall.
try:
    fb_response = facebook_graph.put_wall_post('Hello from Python', \
                                               profile_id = FACEBOOK_PROFILE_ID)#settings.FACEBOOK_PROFILE_ID)
    print fb_response
except facebook.GraphAPIError as e:
    print 'Something went wrong:', e.type, e.message