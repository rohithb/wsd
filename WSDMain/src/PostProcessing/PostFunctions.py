'''
Created on 08-Mar-2013

@author: rohith
'''
from nltk.corpus import wordnet
from PostProcessing.Neo4jDAO import Neo4jDAO
from Parser.models import Dependency
from Parser.depParseFunc import parseSenses

class PostFn:
    '''
    contains all the post processing functions
    '''
    def __init__(self):
        self.neoo4jDAO = Neo4jDAO()
        self.dep = Dependency()
        
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
    
    def fetchAndParseGlossess(self,word):
        '''
        This function will retrieve all the senses for the parameter "word" . 
        Also they are parsed and stores the parse tree along with the weight in to a list
        '''
        syns= wordnet.synsets(word)
        senseList=[]
        for syn in syns:
            senseList.append(syn.definition)
        depParsed = parseSenses(senseList)
        return depParsed
        
            
