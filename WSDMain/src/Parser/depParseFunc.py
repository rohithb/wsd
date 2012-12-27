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

def parseContents(contentList):
    depGraphList=[]
    for content in contentList:
        for s in sent_tokenize(content):
            s=re.sub('[\n\t]',"",s)
            s=urlencode(s)
            url = 'http://nlp.stanford.edu:8080/parser/index.jsp?query='+s
            response = urlopen(url)
            soup=BeautifulSoup(''.join(response.read()))
            collapsedTypedDep =strip_tags(soup.findAll('div',{'class':'parserOutput'})[3])
            collapsedTypedDep =re.sub('[0-9-]+',"",collapsedTypedDep) # to remove numbers and '-'
            rx = re.compile("\((.+), (.+)\)")
            depGraphList.append(rx.findall(collapsedTypedDep))
    return depGraphList