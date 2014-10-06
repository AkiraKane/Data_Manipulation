# -*- coding: utf-8 -*-      
import json, re, os, urllib2
import sys, collections
import sqlite3 as sqlite
import matplotlib.pyplot as plt

from math import sin, cos, sqrt, atan2, radians

def convert(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

############## Utility functions for finding distances via Google Geocode API ##############
# get_lat_long:  Fetch the latitude and longitude of a place name string using the Google geocode API
#
# Input:  name string, e.g. "Ann Arbor, MI"
# Output: a floating-point tuple containing the latitude and longitude, or [None, None] if not found
#
def get_lat_long(place):
    place = re.sub('\s','+', place, flags=re.UNICODE)
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + place
    content = urllib2.urlopen(url).read()

    obj = json.loads(content)
    results = obj['results']

    lat = long = None
    if len(results) > 0:
        loc = results[0]['geometry']['location']
        lat = float(loc['lat'])
        long = float(loc['lng'])

    return [lat, long]

# Great circle distance between two points using the haversine formula
#
# pass the first point's latitude and longitude (in degrees) as a 2-tuple
# pass the second point's latitude and longitude (in degrees) as a 2-tuple
# returns -1 if either input point is invalid, i.e. negative degree values
def great_circle_distance(pt1, pt2):
    R = 6371.0   # mean radius of the Earth in km

    if (pt1[0] < 0 or pt2[0] < 0):
        return -1

    lat1_r = radians(pt1[0])
    lon1_r = radians(pt1[1])
    lat2_r = radians(pt2[0])
    lon2_r = radians(pt2[1])

    dlon = lon2_r - lon1_r
    dlat = lat2_r - lat1_r

    a = (sin(dlat/2))**2 + cos(lat1_r) * cos(lat2_r) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c

    return distance


with sqlite.connect(r'si-601-hw4_tssameer.db') as con:
    cur = con.cursor()
    cur.execute('''SELECT FP.friend_id, FP.hometown_name, FE.school_name, FE.school_level
                    FROM friend_profile FP
                    LEFT JOIN (
                    SELECT friend_id, school_name,
                    CASE WHEN school_type='Graduate School' then 3
                          WHEN school_type='College' then 2
                          WHEN school_type='High School' then 1
                          END as school_level FROM friend_education
                    ) AS FE ON FP.friend_id = FE.friend_id
                    WHERE FP.hometown_name IS NOT NULL;''')
    rows = cur.fetchall()

    rows = convert(rows)

plotdat = dict()
for row in rows:
    temp = list(row)
    try:
        temp.append( great_circle_distance(get_lat_long(row[1]),get_lat_long(row[2])))
    except:
        continue
    xcoord = temp[3]
    ycoord = temp[4]
    if ycoord == -1:
        continue
    if temp[0] in plotdat:
        plotdat[temp[0]][0].append(xcoord)
        plotdat[temp[0]][1].append(ycoord)
    else:
        plotdat[temp[0]] = [[xcoord],[ycoord]]

for line in plotdat:
    plt.plot(plotdat[line][0],plotdat[line][1])
plt.xlabel("School Level")
plt.ylabel("Distance from Hometown")
plt.xlim(0.5, 3.5)
plt.show()