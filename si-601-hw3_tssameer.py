#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json, urllib2, re, time, itertools, pydot

# Step 1

imdb_html = urllib2.urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100')
html1 = imdb_html.read()
html_encoded = html1.decode('utf-8')
step1 = open('step1.html','w')
step1.write(html_encoded.encode('utf-8'))
step1.close()

# Step 2

imdb = open('step1.html','r')
soup = BeautifulSoup(imdb)
tlinks = soup.find_all("td","title")
movdat= []
for link in tlinks:
    movie = []
    iid = link.span.get('data-tconst')
    rank = str(link.parent.find('td','number').text.replace('.',''))
    title = str(link.a.text.encode('utf-8'))
    year = str(link.find('span','year_type').text)
    movie.append(iid)
    movie.append(rank)
    movie.append(title)
    movie.append(year)
    movdat.append(movie)

step2 = open('step2.txt','w')
for mov in movdat:
    step2.write(mov[0] + '\t' + mov[1] + '\t' + mov[2] + ' ' + mov[3] + '\n')
step2.close()

# Step 3
'''
step3 = open('step3.txt','w')
for mov2 in movdat:
    metdatu = urllib2.urlopen('http://www.omdbapi.com/?i=' + mov2[0])
    metdat = metdatu.read().decode('utf-8')
    step3.write(metdat.encode('utf-8') + '\n')
    print mov2[2] + ' Completed'
    time.sleep(5)
step3.close()
'''

# Step 4

step4 = open('step4.txt','w')
jdat = open('step3.txt', 'rU')
for line in jdat :
    dat = json.loads(line)
    nam = str(dat['Title'].encode('utf-8'))
    act = str(dat['Actors'].encode('utf-8')).split(', ')
    jact = json.dumps(act)
    step4.write(nam + '\t' + jact + '\n')
step4.close()


# Step 5
graph = pydot.Dot(graph_type='graph', charset="utf8")
ddat = open('step4.txt', 'rU')
for dat in ddat:
    dat = dat.strip()
    for combo in itertools.combinations([str(i.encode('utf-8')) for i in json.loads(dat.split('\t')[1])],2):
        edge = pydot.Edge(*combo)
        graph.add_edge(edge)
print graph
graph.write("actors_graph_output.dot")
