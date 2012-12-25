'''
Created on 25-Dec-2012

@author: rohith
'''
import string
from nltk.corpus import stopwords
from urllib import urlencode
from urllib2 import urlopen, Request
from BeautifulSoup import BeautifulSoup
from django.utils.html import strip_tags
import re

def removePunctuations(text):
    newText=text.translate(string.maketrans("",""),string.punctuation)
    newText=re.sub('[0-9]+',"",newText)
    return newText

def removeStopWords(splitText):
    filtered_words = [w for w in splitText if not w in stopwords.words('english')]
    return filtered_words

def makeQueryString(text):
    words=removePunctuations(text)
    words=words.split()
    words=removeStopWords(words)
    queryStr=""
    for word in words:
        queryStr+=word + "+"
    queryStr=queryStr[:-1]
    return queryStr
def googleSearch(query):
    url = 'http://www.bing.com/search?q='+query
 #   values = {
 #             'q' : query 
 #             }
 #   data = urlencode(values)
#    req = Request(url,data)
    response = urlopen(url)
    the_page=response.read()
    return the_page
def extractLinks(page):
    soup=BeautifulSoup(''.join(page))
    urlList=[]
    for a in soup.findAll('div',{"class":"sb_tlst"}):
            urlList.append(a.findNext('a').get('href').encode('ascii','ignore')) 
    return urlList

def fetchPages(urlList):
    contents=[]
    for count in range(0,1):
        link=urlList[count]
        req=Request(link,headers={'User-Agent' : "Magic Browser"})
        res=urlopen(req)
        soup=BeautifulSoup(''.join(res.read()))
        try:
            body=strip_tags(soup.html.body)
        except:
            body=strip_tags(res.read())
        # sentenece tokenize  
        body=removePunctuations(body.encode('ascii','ignore'))  # this may cause exclusion of the target word
        contents.append(body)
    return contents
