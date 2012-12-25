'''
Created on 25-Dec-2012

@author: rohith
'''
import string
from nltk.corpus import stopwords
from urllib import urlencode
from urllib2 import Request, urlopen
from BeautifulSoup import BeautifulSoup

def removePunctuations(text):
    newText=text.translate(string.maketrans("",""),string.punctuation)
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
            urlList.append(a.findNext('a').get('href')) 
    return urlList