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


def plat_results(link, platform):
    offset = 0
    tot_results = 100
    limit = 100
    results = []
    while(offset<tot_results):
        response = urllib2.urlopen(link% (access_token, limit, offset,platform))
        json_str = response.read()
        op = convert(json.loads(json_str))
        for r in op['results']:
            results.append(r['name'])
        # for k in op['results']:
        #     print k
        offset += 100
        tot_results = op['number_of_total_results']
        print offset
        sleep(1)
    return results

# #ids for the platforms
# for platform in ['PC','Xbox 360', 'Xbox One', 'PlayStation 3', 'PlayStation 4']:
#     response = urllib2.urlopen('http://www.giantbomb.com/api/platforms/?format=json&api_key=%s&format=json&field_list=name,id&filter=name:%s' % (access_token,platform))
#     json_str = response.read()
#     temp = convert(json.loads(json_str))
#     print json.dumps(temp, indent=4, sort_keys=True)

game_setl = []
for p_id in [94, 145, 146]:
    game_setl.append(set(plat_results('http://www.giantbomb.com/api/games/?format=json&api_key=%s&field_list=name&limit=%i&offset=%i&filter=original_release_date:2013-1-1 00:00:00|2015-1-1 00:00:00,platforms:%i&sort=original_release_date:asc',p_id)))

cmn_games = list(set.intersection(*game_setl))
print len(cmn_games)
print cmn_games

with open("cmn_games3.csv","w") as op:
    out = csv.writer(op)
    for val in cmn_games:
        out.writerow([val])