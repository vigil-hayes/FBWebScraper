import requests
import json
import csv 
import sys 
import subprocess

# Parameters of your app and the id of the profile you want to mess with.
FACEBOOK_APP_ID     = '786517178131951'
FACEBOOK_APP_SECRET = '2e3f91a3f34407fbced1566ee276505c'
page_ids = []


# Trying to get an access token. Very awkward.
oauth_args = dict(client_id     = FACEBOOK_APP_ID,
                  client_secret = FACEBOOK_APP_SECRET,
                  grant_type    = 'client_credentials')
oauth_curl_cmd = ['curl',
                  'https://graph.facebook.com/oauth/access_token?' + urllib.parse.urlencode(oauth_args)]
oauth_response = subprocess.Popen(oauth_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0]

try:
    print(oauth_response)
    print(str(oauth_response))
    oauth_access_token = urllib.parse.parse_qs(str(oauth_response))['access_token']
    #oauth_access_token = "786517178131951|0VSgFwHkhn1yCC50vtQvR1X8A8o"
except KeyError as e:
    print(e)
    print('Unable to grab an access token!')
    exit()
