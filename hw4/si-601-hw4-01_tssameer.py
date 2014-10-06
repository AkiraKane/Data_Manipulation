# -*- coding: utf-8 -*-      
import facebook, urllib2, json, re, os
import sys
import collections,csv

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
access_token = 'CAACEdEose0cBAFoVqwSo3apS4Y9ZCaIHZBIt0288olw2Nqod3BpHVnNlVEglNqPnhZCfEN4wbL4eIxyyZCOEUlkwKUHzNDKNyybZBfStRecfexhYg6SNRpYf1qGjZAcgyERivbfUZCYa1q1qaawKZBeZBarGAGguZB0pLwGAZAKhYKC1S0gw8dScLs18DX5V2kBf2e3nNpxdwZCitYtoFYCjxlj2ZAVqetBf0XI4ZD'

### use Graph API to get friends
graph = facebook.GraphAPI(access_token)
profile = graph.get_object('me')
friends = graph.get_connections('me', 'friends')

i=1
fdat = []
for friend in friends['data']:
    ### get friend details
    response = urllib2.urlopen('https://graph.facebook.com/%s?access_token=%s&fields=gender,birthday,hometown,location,education,checkins' % (friend['id'], access_token))
    json_str = response.read()
    temp = convert(json.loads(json_str))
    fdat.append(temp)
    sleep(2)  # Pause between Facebook API calls
    if i == 100:
        break
    print i,
    i += 1

print len(fdat)

fpl =[]
fel = []
i = 1
for dat in fdat:
    ldat = dict()
    ldat['friend_id'] = i
    if 'gender' in dat:
        ldat['gender'] = dat['gender'][0].upper()
    else:
        ldat['gender'] = None
    if 'birthday' in dat:
        year = re.search(r'\d{4}',dat['birthday'])
        if year:
            ldat['birthyear'] = year.group()
        else:
            ldat['birthyear'] = None
    else:
        ldat['birthyear'] = None
    if 'hometown' in dat:
        ldat['hometown_id'] = dat['hometown']['id']
        ldat['hometown_name'] = dat['hometown']['name']
    else:
        ldat['hometown_id'] = None
        ldat['hometown_name'] = None
    if 'location' in dat:
        ldat['location_id'] = dat['location']['id']
        ldat['location_name'] = dat['location']['name']
    else:
        ldat['location_id'] = None
        ldat['location_name'] = None
    if 'checkins' in dat:
        locs = re.findall(r'location', str(dat['checkins']))
        ldat['checkins'] = len(locs)
    else:
        ldat['checkins'] = None
    fpl.append(ldat)
    if 'education' in dat:
        for ed in dat['education']:
            edat = dict()
            edat['friend_id'] = i
            edat['school_id'] = ed['school']['id']
            edat['school_name'] = ed['school']['name']
            edat['school_type'] = ed['type']
            fel.append(edat)
    i += 1



cnames1 = ['friend_id','gender','birthyear','hometown_id','hometown_name','location_id','location_name','checkins']
fpcsv = open('friend_profile_tssameer.csv','wb')
fp_writer = csv.DictWriter(fpcsv, cnames1)
fp_writer.writerows(fpl)


cnames2 = ['friend_id','school_id','school_name','school_type']
fecsv = open('friend_education_tssameer.csv','wb')
fe_writer = csv.DictWriter(fecsv, cnames2)
fe_writer.writerows(fel)

fpcsv.close()
fecsv.close()
