from django.db import models

# Create your models here.

class Dependency:
    '''
    model class for inserting relations in the database
    '''
    __parent = None
    __child = None
    __rel = None
    
    def setParent(self,parent):
        self.__parent = parent
    def getParent(self):
        return self.__parent
    
    def setChild(self,child):
        self.__child = child
    def getChild(self):
        return self.__child
    
    def setRel(self,rel):
        self.__rel = rel
    def getRel(self):
        return self.__rel
        

