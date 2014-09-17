__author__ = 'Sameer'

import re
from collections import Counter

aclog = open('/home/sameer/access_log.txt','rU')

pattern = r'^\S+ . . \[(.+)\] "(.*)" (\d+) \S+ "(.*)" ".*"'
pattern2 = r'(GET|POST) https?:\/\/[a-zA-Z]'
pattern3 = r'\d{2}\/\w{3}\/\d{4}'
i = 1
datdom = dict()
invlog = dict()
for log in aclog:
    match1 = re.search(pattern, log)
    if ('GET' in match1.group(2) or 'POST' in match1.group(2)) and match1.group(3) == '200':
        if re.match(pattern2,match1.group(2)):
            temp = re.search(r'https?:\/\/[a-zA-Z]([\w\.-])+(?<=\.)([a-zA-Z]+)(.+)?',match1.group(2))
            date = re.search(pattern3,match1.group(1))
            try:
                if date.group() in datdom:
                    datdom[date.group()] = str(temp.group(2)).lower() + ' ' + datdom[date.group()]
                else:
                    datdom[date.group()] = str(temp.group(2)).lower()
            except:
                invlog[match1.group(1) + str(i)] = log
                i += 1
        else:
            invlog[match1.group(1) + str(i)] = log
            i += 1
    else:
        invlog[match1.group(1) + str(i)] = log
        i += 1

invdat = open('invalid_access_log_tssameer.txt', 'w')
for k in sorted(invlog):
    invdat.write(invlog[k])
invdat.close()

logsum = open('valid_log_summary_tssameer.txt', 'w')
for key in sorted(datdom):
    logdict = dict((Counter(datdom[key].split()).items()))
    logsum.write( key )
    for key2 in sorted(logdict):
        logsum.write('\t' + key2 + ':' + str(logdict[key2]))
    logsum.write('\n')
logsum.close()
