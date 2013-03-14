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
    typedDep=""
    depGraphList=[]
    str1=[]
    str1.append('.'.join(contentList)) # to make the whole list into a single item
                                        # otherwise the parser need to be initialised many times.
    parser = StanfordParser ("/home/rohith/stanford-parser")
    for content in str1:
        typedDep += parser.parse(content)
        typedDep =re.sub('[0-9-]+',"",typedDep) # to remove numbers and '-'
        rx = re.compile("\((.+), (.+)\)")
        depGraphList.append(rx.findall(typedDep))
        # import string
        #string.split(inputString, '\n')  # --> ['Line 1', 'Line 2', 'Line 3']    
    return depGraphList

def parseSenses(senseList):
    typedDep=""
    depGraphList=[]
    tempList=[]
    str1=[]
    str1.append('.'.join(senseList)) # to make the whole list into a single item
                                        # otherwise the parser need to be initialised many times.
    parser = StanfordParser ("/home/rohith/stanford-parser")
    for content in str1:
        typedDep += parser.parse(content)
        typedDep =re.sub('[0-9-]+',"",typedDep) # to remove numbers and '-'
        #need to separate each senses into induvidual lists
        typedDepList = typedDep.split("\n\n")
        rx = re.compile("\((.+), (.+)\)")
        for dep in typedDepList:
            depGraphList.append(rx.findall(dep))   
    return depGraphList
