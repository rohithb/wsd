'''
Created on 08-Mar-2013

@author: rohith
'''
from nltk.corpus import wordnet
from PostProcessing.Neo4jDAO import Neo4jDAO
from Parser.models import Dependency
from Parser.depParseFunc import parseSenses, parseContents
from nltk.compat import defaultdict

class PostFn:
    '''
    contains all the post processing functions
    '''
    def __init__(self):
        self.neoo4jDAO = Neo4jDAO()
        self.dep = Dependency()
        self.wt={}
        
    def insertToDB(self,depGraphList):
        '''
        Extract each pair of words from the dependency list , 
        calculate the chi-square value and insert to the database. 
        :param depGraphList : list - representation of dependency graph.
                             eg : [[(word1,word2),(word3,word4)...],[(wordi),(wordi+1) ...],...]
        '''        
        for dlist in depGraphList:
            for dtuple in dlist:
                parent = dtuple[0]
                child = dtuple[1]  
                rel = self._chiSq(parent, child)
                self.dep.setAll(parent, child, rel)
                self.neoo4jDAO.insert(self.dep)
        
    def _chiSq(self, word1, word2):
        '''
        calculate the chi-square value of word1 and word2.
        :param word1 : string - first word 
        :param word2 : string - second word
        :return value: chi-square value of word1 and word2
        '''
        try:
            syn1 = wordnet.synsets(word1)[0]
            syn2 = wordnet.synsets(word2)[0]
            rel = syn1.wup_similarity(syn2)
        except:
            rel = 0.0050 # threshold for chi-square test
        return rel
    
    def fetchSenses(self, wsdWord):
        '''
        fetches all senses from wordnet corresponding to wsdWord
        return 0 if the word is not found in wordNet
        '''
        syns= wordnet.synsets(wsdWord)
        senseList=[]
        for syn in syns:
            senseList.append(syn.definition)
        return senseList
        
    def createSenseTree(self, senseList):
        '''
        Retrieve all the senses for the parameter "word" from wordnet . 
        Return the dependency graphs of senses (defaultDict)
        eg: {'conduct': ['institution', 'to', 'business'], 
        'ROOT': ['created'], 'institution': ['an'], 'created': ['institution', 'conduct']}
        '''
        senseDict = []
        depParsed = parseSenses(senseList)
        for dep in depParsed:
            temp = defaultdict( list )
            for n ,v in dep:
                temp[n].append(v)
            senseDict.append(temp)
        return senseDict
    
    def createWSDTextTree(self, wsdText):
        '''
        create parse tree for the wsdText.
        wsdText should be a single sentence.
        Else only parse tree of first sentence will be returned  
        '''
        tempList = []
        tempList.append(wsdText)
        tempDict = self.createSenseTree(tempList) # avoiding unnecessary 2d list :-)
        return tempDict[0]

    def calulateWeightSense(self,parent, level,l):
        if(level == 1 and parent == 'ROOT'):
            return
        if(level == 0):
            self.wt={}
        level+=1
        a=l[parent]
        if(len(a) != 0):
            for i in a:
                self.wt[i]=1.0/level
                self.fun(i,level,l)
        return self.wt
    

    def depScore(self, senseList, senseTrees, wsdTextTree):
        '''
        calculate DepScore and return the index number of the sense with largest DepScore
        Process: Search the KB for each word in each sense
        '''
        #search the KB for each word in each sense
        score = []
        for sense in senseList:
            sense = sense.split()
            for word in sense:
                deps = self.neoo4jDAO.findDependent(word) 
                if(len(deps) != 0):
                    
                    
                    
                    
                       
                    