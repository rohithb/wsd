'''
Created on 08-Mar-2013

@author: rohith
'''
from nltk.corpus import wordnet
from PostProcessing.Neo4jDAO import Neo4jDAO
from Parser.models import Dependency
from Parser.depParseFunc import parseSenses, parseContents
from nltk.compat import defaultdict
from nltk.collocations import BigramAssocMeasures

class PostFn:
    '''
    contains all the post processing functions
    '''
    def __init__(self):
        self.neoo4jDAO = Neo4jDAO()
        self.dep = Dependency()
        self.wt={}
        self.temp = 0
        
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
                rel = self._chiSq(depGraphList,parent, child)
                self.dep.setAll(parent, child, rel)
                self.neoo4jDAO.insert(self.dep)
        
#    def _chiSq(self, word1, word2):
#        '''
#        calculate the chi-square value of word1 and word2.
#        :param word1 : string - first word 
#        :param word2 : string - second word
#        :return value: chi-square value of word1 and word2
#        '''
#        try:
#            syn1 = wordnet.synsets(word1)[0]
#            syn2 = wordnet.synsets(word2)[0]
#            rel = syn1.wup_similarity(syn2)
#        except:
#            rel = 0.0050 # threshold for chi-square test
#        if(rel == -1):
#            rel = 0.0050
#        return rel
    
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
                self.calulateWeightSense(i,level,l)
        return self.wt
    
    def calulateWeightSense1(self,parent, level,l):
        if(level == self.temp and parent == 'ROOT'):
            return
        if(level == self.temp-1):
            self.wt={}
        level+=1 
        a=l[parent]
        if(len(a) != 0):
            for i in a:
                self.wt[i]=1.0/level
                self.calulateWeightSense(i,level,l)
        return self.wt
    

    def depScore(self, senseList, wsdText, wsdWord, senseTrees, wsdTextTree):
        '''
        calculate DepScore and return the index number of the sense with largest DepScore
        Process: Search the KB for each word in each sense
        '''
        #search the KB for each word in each sense
        score = []
        l = len(senseList)
        wsdText = wsdText.split()
        wtWSDText = self.calculateWeightWSDText(wsdWord, wsdTextTree)
        for i in range(0,l):
            tempScore = 0.0
            wtSense = self.calulateWeightSense('ROOT', 0, senseTrees[i])
            sense = senseList[i].split()
            for word in sense:
                deps = self.neoo4jDAO.findDependent(word)
                if(deps != None):
                    for tup in deps:
                        if(str(tup[0]) in wsdText):
                            node = str(tup[0])
                            wts=wtSense[word]
                            wtt =wtWSDText[node]
                            tempScore += tup[1]* wts* wtt
                else:
                    continue
            score.append(tempScore)
        return score.index(max(score))
    
    def glossScore(self, senseList, wsdText, wsdWord ,senseTrees, wsdTextTree ):
        score =[]
        l = len(senseList)
        wsdText = wsdText.split()
        wtWSDText = self.calculateWeightWSDText(wsdWord, wsdTextTree)
        for i in range(0,l):
            tempScore = 0.0
            wtSense = self.calulateWeightSense('ROOT', 0, senseTrees[i])
            sense = senseList[i].split()   
            for word in sense:
                if(word in wsdText):
                    tempScore += wtSense[word] + wtWSDText[word]
            score.append(tempScore)
        return score.index(max(score))
    
    def getLevel(self,word,tree,parent, level):
        if(level == 1 and parent == 'ROOT'):
            return 
        level+=1
        a=tree[parent]
        if(len(a) != 0):
            for i in a:
                if(i == word):
                    self.temp = level
                self.getLevel(word,tree,i,level)
        return self.temp
    
    def calculateWeightWSDText(self, word, tree):
        self.wt = {}
        temp ={}
        wtTemp = self.calulateWeightSense(word, 0, tree)
        temp.update(wtTemp)
        level = self.getLevel(word, tree, 'ROOT', 0)
        level -= 1
        wtt = self.calulateWeightSense1("ROOT", level, tree)
        wtt.update(temp)
        return wtt
        
    def _chiSq(self,depGraphList, word1 ,word2):
        bigram_measures = BigramAssocMeasures()
    
        firstTuple = word1
        secondTuple = word2
        depLength = len(depGraphList)
            # value of n11
        i = 0
        j = 0
        count1 = 0
        count2 = 0
        count3 = 0
        for j in range(depLength):
            if (firstTuple == depGraphList[i][0] or firstTuple == depGraphList[i][1]) and (secondTuple == depGraphList[i][0] or secondTuple == depGraphList[i][1]):    
                count1 = count1+1
            else:
                count1 = count1
            i = i+1
            j = j+1
        cnt1 = count1
        
            # value of n12
        i = 0
        j = 0
    
        for j in range(depLength):
            if firstTuple == depGraphList[i][0] or firstTuple == depGraphList[i][1]:
                count2 = count2+1
            else:
                count2 = count2
            i = i+1
            j = j+1
        cnt2 = count2-1
    
            #value of n21
        i = 0
        j = 0
    
        for j in range(depLength):
            if secondTuple == depGraphList[i][0] or secondTuple == depGraphList[i][1]:
                count3 = count3+1
            else:
                count3 = count3
            i = i+1
            j = j+1
        cnt3 = count3-1
        
    
            #value of n22
        cnt4 = depLength-cnt1-cnt2-cnt3
    
    
            #total of n11 & n12
        n1p = cnt1+cnt2
        
            #total of n21 & n22
        n2p = cnt3+cnt4
        
    
            #total of n11 & n21
        np1 = cnt1+cnt3
    
            
            #total of n12 & n22
        np2 = cnt2+cnt4
    
        
        
                            # Equatio of chi square test=> X^2 = [N(n11 * n22 - n12 * n21)^2]/[n1. * n2. * n.1 * n.2]
        
        
        x2 = '%0.4f' % bigram_measures.chi_sq(cnt1,(np1,n1p),depLength)
        
        return x2
                    
                    
                       
                    