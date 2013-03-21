# Create your views here.
from nltk.tokenize import sent_tokenize, word_tokenize
from django.http import HttpResponse
from nltk.corpus import wordnet as wn
from Parser.depParseFunc import parseContents
from Parser.StanfordParser import StanfordParser
from PreProcessing.PreFunctions import makeQueryString, googleSearch,\
    extractLinks, fetchSentsFromPages, stemWords, setStatus
from PostProcessing.PostFunctions import PostFn
from django.contrib import messages
from django.utils.html import strip_tags

def makeGraph(request):
    stat_file = open("/home/rohith/stat.txt")
    ret = stat_file.read()
    return HttpResponse(ret)

def doWSD(request):
    postFn= PostFn()
    if 'wsdText' in request.POST:
        wsdText =request.POST['wsdText']  # modify in index.html to send only the sentence instead of whole text
    else:
        wsdText = ''
    if 'wsdWord' in request.POST:
        wsdWord =request.POST['wsdWord']
    else:
        wsdWord = ''
    if 'updateKB' in request.POST:
        updateKB = request.POST['updateKB']
    wsdText = wsdText.lower()
    wsdWord = wsdWord.lower()
    wsdText = strip_tags(wsdText)
    
    wsdText = stemWords(wsdText)
    wsdWord = stemWords(wsdWord)
    if(updateKB == "on"):
        setStatus("Making Query String")
        queryStr = makeQueryString(wsdText)
        setStatus("Searching on Yahoo.com")
        page = googleSearch(queryStr)
        setStatus("Extracting Links From Result")
        urlList = extractLinks(page)
        setStatus("Fetching Contents")
        contents=fetchSentsFromPages(urlList)
        setStatus("Parsing Contents")
        depGraphList=parseContents(contents)
        setStatus("Updating knowledgebase")
        postFn.insertToDB(depGraphList)
    setStatus("Fetching Senses")
    senseList = postFn.fetchSenses(wsdWord)
    setStatus("Creating Sense Parse Trees")
    senseTrees = postFn.createSenseTree(senseList)
    setStatus("Creating Parse Tree for Input")
    wsdTextTree = postFn.createWSDTextTree(wsdText)
    setStatus("Calculating Dep Score")
    candidateSense1 = postFn.depScore(senseList, wsdText, wsdWord, senseTrees, wsdTextTree)
    setStatus("Calculating Gloss Score")
    candidateSense2 = postFn.glossScore(senseList, wsdText, wsdWord , senseTrees, wsdTextTree)
    if(candidateSense1 == candidateSense2):
        sense = candidateSense1
    else:
        if(candidateSense1 > candidateSense2):
            sense = candidateSense2
        else:
            sense = candidateSense1
    html = postFn.createMarkup(senseList[sense],wsdText,wsdWord)
    return HttpResponse(html)
    