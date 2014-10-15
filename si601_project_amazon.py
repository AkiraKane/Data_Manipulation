# -*- coding: utf-8 -*-
#!/usr/bin/python

#Associates ID = si6profal201-20
#Access Key ID = AKIAJEQW5HURL3O4L5HA
# AWSAccessKeyId=AKIAIJF7EL6HPGZO363Q
# AWSSecretKey=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

from time import sleep
from bs4 import BeautifulSoup
import urllib2,csv
from lxml import objectify, etree
from amazonproduct import API
api = API(locale='us')

cmn_games = []
with open('cmn_games.csv', 'r') as op:
    cmn_gms = csv.reader(op)
    for row in cmn_gms:
        cmn_games.extend(row)

print len(cmn_games)

game_list = []
for game in cmn_games:
    for plt in ['PC', 'Xbox One', 'Playstation 4']:
        game_dict = dict()
        game_dict['Title'] = game
        game_dict['Platform'] = plt
        try:
            print game + ' ' + plt + '\n'
            ress = api.item_search('VideoGames', Keywords=game + ' ' + plt)
            for res in ress:
                root = res
                # xml_new = etree.tostring(root, pretty_print=True)
                # print xml_new
                game_dict['Amzn_Title'] = root.ItemAttributes.Title
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
                    game_dict['Rating'] = soup.find_all("div","crIFrameNumCustReviews")[0].find('img').get('title')
                    no_reviews = soup.find_all("div","crIFrameNumCustReviews")[0].span.text
                    for ch in ['\n','(',')']:
                        no_reviews = no_reviews.replace(ch,'')
                    game_dict['Reviews'] = no_reviews
                    print game_dict
                    game_list.append(game_dict)
                except:
                    print 'also lol'
                break
        except:
            print 'lol'

print len(game_list)
print game_list

cnames = ['Title','Platform','Amzn_Title','Price','Rating','Reviews']
cgs = open('cm_gm_dat.csv','wb')
fp_writer = csv.DictWriter(cgs, cnames)
fp_writer.writerows(game_list)

# print etree.tostring(result, pretty_print=True)
# for e in root.iterchildren():
#     print e.tag


# for t in temp:
#     print etree.tostring(t, pretty_print=True)