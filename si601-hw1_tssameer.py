#!/usr/bin/python -tt
__author__ = 'Sameer'
import csv
from math import log

wbi = open('/home/sameer/world_bank_indicators.txt','rU')
wbiclms = wbi.readline().split('\t')

wbi_list = []

for arow in wbi:
    rowt = arow.split('\t')
    rowd = dict()
    if '2000' in rowt[1] or '2010' in rowt[1]:
        rowd['Country Name'] = rowt[0]
        rowd['Date'] = rowt[1]
        rowd['Total population'] = rowt[9].strip('"')
        rowd['Mobile subscribers'] = rowt[4].strip('"')
        rowd['Health: mortality under-5'] = rowt[6]
        rowd['Internet users per 100 people'] = rowt[5]
        rowd['GDP per capita'] = rowt[19].replace('\n','').strip('"')
        if not ('' in rowd.values()):
            rowd['Mobile subscribers per capita'] = '{:.5f}'.format(float(rowt[4].replace(',', '').strip('"'))/float(rowt[9].replace(',', '').replace('"','').strip('"')))
            rowd['log(GDP per capita)'] = '{:.5f}'.format(log(int(rowt[19].replace(',', '').replace('\n','').strip('"'))))
            rowd['log(Health: mortality under 5)'] = '{:.5f}'.format(log(int(rowt[6].replace(',', '').strip('"'))))
            wbi_list.append(rowd)

wbr = open('/home/sameer/world_bank_regions.txt','rU')
wbrclms = wbr.readline().split('\t')

locd = dict()
for locdat in wbr:
    loct = locdat.split('\t')
    locd[loct[2].replace('\n','')] = loct[0]

# Added a couple of the missing countries
locd['West Bank and Gaza'] = 'Asia'
locd['Tuvalu'] = 'Oceania'

for datad in wbi_list:
    try:
        datad['Region'] = locd[datad['Country Name']]
    except:
        datad['Region'] = ''

wbdat = sorted(wbi_list, key=lambda x: (x['Date'][-4:],x['Region'],int(x['GDP per capita'].replace(',', ''))))

cnames = ['Country Name', 'Date', 'Total population', 'Mobile subscribers', 'Health: mortality under-5', 'Internet users per 100 people', 'GDP per capita', 'Mobile subscribers per capita', 'log(GDP per capita)', 'log(Health: mortality under 5)', 'Region']

wbcsv = open('worldbank_output_tssameer.csv','wb')
wb_writer = csv.DictWriter(wbcsv, cnames)
wb_writer.writer.writerow(cnames)
wb_writer.writerows(wbdat)

wbcsv.close()
wbr.close()
wbi.close()