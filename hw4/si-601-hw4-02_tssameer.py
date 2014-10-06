#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'sameer'

import csv,collections
import sqlite3 as sqlite

def convert(data):
    if isinstance(data, basestring):
        return data.decode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

with open('friend_profile_tssameer.csv','rU') as fpcsv:
    fplot = [tuple([k if k is not '' else None for k in dat]) for dat in csv.reader(fpcsv)]

fplot = convert(fplot)

with sqlite.connect(r'si-601-hw4_tssameer.db') as con:
  cur = con.cursor()
  cur.execute("DROP TABLE IF EXISTS friend_profile")

  cur.execute('''CREATE TABLE IF NOT EXISTS friend_profile
              (friend_id INT ,
               gender TEXT,
               birthyear INT,
               hometown_id INT,
               hometown_name TEXT,
               location_id INT,
               location_name TEXT,
               checkins INT)''')

  cur.executemany("INSERT INTO friend_profile VALUES(?, ?, ?, ?, ?, ?, ?, ?)", fplot)
  con.commit()


with open('friend_education_tssameer.csv','rU') as fecsv:
    felot = [tuple([k if k is not '' else None for k in dat]) for dat in csv.reader(fecsv)]

felot = convert(felot)

with sqlite.connect(r'si-601-hw4_tssameer.db') as con:
  cur = con.cursor()
  cur.execute("DROP TABLE IF EXISTS friend_education")

  cur.execute('''CREATE TABLE IF NOT EXISTS friend_education
              (friend_id INT ,
               school_id INT,
               school_name TEXT,
               school_type TEXT)''')

  cur.executemany("INSERT INTO friend_education VALUES(?, ?, ?, ?)", felot)
  con.commit()
