#!/usr/bin/python

### python si-601-lab-5.py input-v2.txt

from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w]+")
f = open(r'si601_lab5_output_tssameer.txt', 'w')

class BiGramFreqCount(MRJob):
  ### input: self, ignored_key, in_value
  def mapper(self, _, line):
      words = WORD_RE.findall(line)
      for i in range(len(words)-1):
          exp = r"\b"+words[i]+r"[.,-\?/!\|/(/)/'"+'/"'+ "/ ]+"+words[i+1]+r"\b"
          test = re.compile(exp)
          res = test.search(line)
          if res:
              ans = words[i]+' '+words[i+1]
              yield (ans.lower(),1)

    
  ### input: self, in_key from mapper, in_value from mapper
  def reducer(self, key, values):
      f.write('"' + str(key) + '"\t'+ str(sum(values)) + '\n')


if __name__ == '__main__':
  BiGramFreqCount.run()

f.close()
