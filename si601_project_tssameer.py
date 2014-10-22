import urllib2, json, re, collections, csv
from time import sleep

access_token = '628bfb5b1daf49082ccce4de40702548fdb8e3d8'


def convert(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data


def results(link):
    offset = 0
    tot_results = 100
    limit = 100
    while(offset<tot_results):
        response = urllib2.urlopen(link% (access_token, limit, offset))
        json_str = response.read()
        op = convert(json.loads(json_str))
        for k in op['results']:
            print k
        print '\nLOL\n'
        offset += 100
        tot_results = op['number_of_total_results']
        print tot_results
        sleep(3)


#response = urllib2.urlopen('http://www.giantbomb.com/api/search/?api_key=%s&format=json&resources=game&limit=100&field_list=name,aliases,id,platforms&query=%s' % (access_token, game_name))

#ids for the platforms
#response = urllib2.urlopen('http://www.giantbomb.com/api/platforms/?format=json&api_key=%s&format=json&field_list=name,id' % (access_token))

results('http://www.giantbomb.com/api/games/?format=json&api_key=%s&field_list=name,number_of_user_reviews&limit=%i&offset=%i&&filter=original_release_date:1980-1-1 00:00:00|1990-1-1 00:00:00,platforms:94&sort=original_release_date:asc')

'''
print temp
print no_results

for k in temp['results']:
   print k'''
#print json.dumps(temp, indent=4, sort_keys=True)