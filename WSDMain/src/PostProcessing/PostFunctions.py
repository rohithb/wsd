'''
Created on 08-Mar-2013

@author: rohith
'''
from nltk.corpus import wordnet
from PostProcessing.Neo4jDAO import Neo4jDAO
from Parser.models import Dependency

class postFn:
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
        
    def chiSq(self, word1, word2):
        '''
        calculate the chi-square value of word1 and word2.
        :param word1 : string - first word 
        :param word2 : string - second word
        :return value: chi-square value of word1 and word2
        '''
        
        syn1 = wordnet.synsets(word1)[0]
        syn2 = wordnet.synsets(word2)[0]
        rel = syn1.wup_similarity(syn2)
        return rel