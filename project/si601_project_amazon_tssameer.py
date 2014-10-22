# -*- coding: utf-8 -*-
#!/usr/bin/python

from time import sleep
from bs4 import BeautifulSoup
import urllib2,csv, collections, re
from amazonproduct import API

#Function to encode data
def convert(data):
    if isinstance(data, basestring):
        return data.encode('utf-8')
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

#Using USA as the location for the API
api = API(locale='us')

cmn_games = []
with open('cmn_games.csv', 'r') as op:
    cmn_gms = csv.reader(op)
    for row in cmn_gms:
        cmn_games.extend(row)

print len(cmn_games)

#A nested loop with all the queries to get the details for each of the games
game_list = []
for game in cmn_games:
    for plt in ['PC', 'Xbox One', 'Playstation 4']:
        game_dict = dict()
        game_dict['Title'] = game
        game_dict['Platform'] = plt
        try:
            print game + ' ' + plt
            res = api.item_search('VideoGames', Keywords=game + ' ' + plt)
            for root in res:
                game_dict['Amzn_Title'] = convert(str(root.ItemAttributes.Title))
                asin = root.ASIN.text
                sleep(2)
                result0 = api.item_lookup(asin,ResponseGroup='OfferSummary')
                game_dict['Price'] = result0.Items.Item.OfferSummary.LowestNewPrice.FormattedPrice.text
                sleep(2)
                result = api.item_lookup(asin,ResponseGroup='Reviews', TruncateReviewsAt=10)
                review_link = result.Items.Item.CustomerReviews.IFrameURL.text
                response = urllib2.urlopen(review_link).read()
                soup = BeautifulSoup(response)
                try:
                    rating = soup.find_all("div","crIFrameNumCustReviews")[0].find('img').get('title')
                    game_dict['Rating'] = rating[:3]
                    no_reviews = soup.find_all("div","crIFrameNumCustReviews")[0].span.text
                    for ch in ['\n','(',')']:
                        no_reviews = no_reviews.replace(ch,'')
                    no_reviews = convert(re.findall(r'\d+',no_reviews)[0])
                    game_dict['Reviews'] = no_reviews
                    print game_dict
                    game_list.append(game_dict)
                except:
                    print 'Rating data missing'
                break
        except:
            print 'Data missing'

print len(game_list)


cnames = ['Title','Platform','Amzn_Title','Price','Rating','Reviews']
with open('cmn_gm_dat_test.csv','wb') as cgs:
    fp_writer = csv.DictWriter(cgs, cnames)
    fp_writer.writerows(game_list)