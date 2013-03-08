from django.db import models

# Create your models here.

class dependency:
    __parent = None
    __child = None
    __dep = None
    
    def setParent(self,parent):
        self.__parent = parent
    def getParent(self):
        return self.__parent
    def setChild(self,child):
        self.__child = child
    def getChild(self):
        return self.__child
    def setDep(self,dep):
        self.__dep = dep
    def getDep(self):
        return self.__dep
        

