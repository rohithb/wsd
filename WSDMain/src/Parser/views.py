# Create your views here.
from nltk.tokenize import sent_tokenize, word_tokenize
from django.http import HttpResponse
from nltk.corpus import wordnet as wn
from Parser.functions import makeQueryString, googleSearch, extractLinks

def makeGraph(request):
    if 'wsdText' in request.POST:
        text =request.POST['wsdText']
    else:
        text = ''
    if 'wsdWord' in request.POST:
        word =request.POST['wsdWord']
    else:
        word = ''
        
    for t in sent_tokenize(text):
        sentence_tokens=word_tokenize(t)
    html=""
    for t in sentence_tokens:
        try:
            syn= wn.synsets(t)
            definition= syn[1].definition
        except:
            definition="Not listed in wordnet"
        html+=t + ' : ' + definition +' </br></br>'
    return HttpResponse(html)

def doWSD(request):
#   if 'wsdText' in request.POST:
#        wsdText =request.POST['wsdText']
#    else:
#        text = ''
#    if 'wsdWord' in request.POST:
#        wsdWord =request.POST['wsdWord']
#    else:
#        word = ''
#       """
    wsdText = "A large company needs a sustainable business model."
    wsdWord="company"
    
   # wsdText=wsdText.encode("ascii")
    queryStr = makeQueryString(wsdText)
    page = googleSearch(queryStr)
    urlList=extractLinks(page)
    html=""
    for l in urlList:
        html+=l+"</br>"
    return HttpResponse(html)
    
    