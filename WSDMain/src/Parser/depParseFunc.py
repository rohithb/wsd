'''
Created on 25-Dec-2012

@author: rohith
'''

from urllib2 import urlopen
import BeautifulSoup
from django.utils.html import strip_tags
import re
from urllib import urlencode
from nltk.tokenize import sent_tokenize
from Parser.StanfordParser import StanfordParser

def parseContents(contentList):
    
    depGraphList=[]
    for content in contentList:
        for s in sent_tokenize(content):
            s=re.sub('[\n\t]',"",s)
            parser = StanfordParser("/home/rohith/stanford-parser/")
            typedDep = parser.parse(s)
            typedDep =re.sub('[0-9-]+',"",typedDep) # to remove numbers and '-'
            rx = re.compile("\((.+), (.+)\)")
            depGraphList.append(rx.findall(typedDep))
    return depGraphList