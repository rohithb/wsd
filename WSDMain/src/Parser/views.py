# Create your views here.
from nltk.tokenize import sent_tokenize, word_tokenize
from django.http import HttpResponse
from nltk.corpus import wordnet as wn
from Parser.depParseFunc import parseContents
from Parser.StanfordParser import StanfordParser
from PreProcessing.PreFunctions import makeQueryString, googleSearch,\
    extractLinks, fetchSentsFromPages, stemWords
from PostProcessing.PostFunctions import PostFn


def makeGraph(request):
    if 'wsdText' in request.POST:
        text =request.POST['wsdText']
    else:
        text = ''
    if 'wsdWord' in request.POST:
        word =request.POST['wsdWord']
    else:
        word = ''
    """    
    for t in sent_tokenize(text):
        sentence_tokens=word_tokenize(t)
    html=""
    for t in sentence_tokens:
        try:
            syn = wn.synsets(t)
            definition= syn[1].definition
        except:
            definition="Not listed in wordnet"
        html+=t + ' : ' + definition +' </br></br>'
    """
    parser = StanfordParser ("/home/rohith/stanford-parser")
    g= parser.parse(text)
    return HttpResponse(g)

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
    wsdText = wsdText.lower()
    wsdWord = wsdWord.lower()
    
    wsdText = stemWords(wsdText)
    wsdWord = stemWords(wsdWord)
    
#    wsdText = "A large company needs a sustainable business model."
#    wsdWord="company"
    
#    convert everything to small case
    queryStr = makeQueryString(wsdText)
    page = googleSearch(queryStr)
    print "GOOGLE SEARCH"
    urlList = extractLinks(page)
    print "FETCHING CONTENTS"
    contents=fetchSentsFromPages(urlList)
#    contents = []
#    test = """mw.loader.using ext.centralNotice.bannerController function mw.centralNotice.initialize Sustainable business From Wikipedia the free encyclopedia Jump to navigation search Sustainable business or green business is an enterprise to be that has minimal negative impact on the global or local environment community society or economya business that strives to meet the triple bottom line. Often sustainable businesses have progressive environmental and human rights policies. In general business is described as green if it matches the following four criteria It incorporates principles of sustainability into each of its business decisions. It supplies environmentally friendly products or services that replaces demand for nongreen products andor services. It is greener than traditional competition. It has made an enduring commitment to environmental principles in its business operations. A sustainable business is any organization that participates in environmentally friendly or green activities to ensure that all processes products and manufacturing activities adequately address current environmental concerns while maintaining a profit. In other words it is a business that meets the needs of the present world without compromising the ability of the future generations to meet their own needs. It is the process of assessing how to design products that will take advantage of the current environmental situation and how well a companys products perform with renewable resources. The Brundtland Report emphasized that sustainability is a threelegged stool of people planet and profit. Sustainable businesses with the supply chain try to balance all three through the triplebottomline conceptusing sustainable development and sustainable distribution to affect the environment business growth and the society. Everyone affects the sust"""
#    test.lower()
#    contents.append(test)
    
    depGraphList=parseContents(contents)
    print "ADDING TO DB"
    postFn.insertToDB(depGraphList)
    senseList = postFn.fetchSenses(wsdWord)
    senseTrees = postFn.createSenseTree(senseList)
    wsdTextTree = postFn.createWSDTextTree(wsdText)
    candidateSense1 = postFn.depScore(senseList, wsdText, wsdWord, senseTrees, wsdTextTree)
    candidateSense2 = postFn.glossScore(senseList, wsdText, wsdWord , senseTrees, wsdTextTree)
    if(candidateSense1 == candidateSense2):
        sense = candidateSense1
    else:
        if(candidateSense1 > candidateSense2):
            sense = candidateSense1
        else:
            sense = candidateSense2
    html = '<h4 style="color:white">'+ wsdWord + ' : ' + senseList[sense] + ' </h4>'
    return HttpResponse(html)
    