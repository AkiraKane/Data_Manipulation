#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'sameer'

import csv,collections
import sqlite3 as sqlite

with sqlite.connect(r'si-601-hw4_tssameer.db') as con:
    cur = con.cursor()
    cur.execute('''SELECT FP.friend_id, IFNULL(FP.checkins, 0),IFNULL(MAX(FE.school_level),0)
                    FROM friend_profile FP
                    LEFT JOIN (
                    SELECT friend_id, school_name,
                    CASE WHEN school_type='Graduate School' then 3
                    WHEN school_type='College' then 2
                    WHEN school_type='High School' then 1
                    END as school_level FROM friend_education
                    ) AS FE ON FP.friend_id = FE.friend_id
                    GROUP BY FP.friend_id;''')
    rows = cur.fetchall()

    with open('friend_join_tssameer.csv','w') as fj:
        fjcsv=csv.writer(fj)
        fjcsv.writerow(['friend_id','checkins','max_school_level'])
        for row in rows:
            fjcsv.writerow(row)