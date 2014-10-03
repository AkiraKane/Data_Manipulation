# -*- coding: utf-8 -*-      
import facebook, urllib2, json, re, os
import sys
import collections

from time import sleep

def convert(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


### Example code to access the Facebook API
### Put your access token in the string variable:
access_token = 'CAACEdEose0cBAJMM7cSzqpq4LSq7h6D7rbHvIP2yoRjsjDOxMuUFXcXJ0Ya6Rgpu6eQ2Ou6gU5jcckvvAEX6YZCZCVeyahkxsJPb14NIG99ZBVa3d1GyRDCaIvapmJLHfcFIMLRSv5COhgkf7DVzWJRpftA3GbvKbuEJpGsppMK2fBr0JpLBdg2O3mGmq28PztNeLt1V8P9xq5V3w3ONZAhaAT56kGIZD'

### use Graph API to get friends
graph = facebook.GraphAPI(access_token)
profile = graph.get_object('me')
friends = graph.get_connections('me', 'friends')

print len(friends['data'])

i=1
for friend in friends['data']:
    ### get friend details
    response = urllib2.urlopen('https://graph.facebook.com/%s?access_token=%s&fields=gender,birthday,hometown,location,education,checkins' % (friend['id'], access_token))
    json_str = response.read()
    temp = convert(json.loads(json_str))
    print (temp)
    sleep(2)  # Pause between Facebook API calls
    i += 1
    if i == 10:
        break
