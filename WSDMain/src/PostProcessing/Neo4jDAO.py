'''
Created on 08-Mar-2013

@author: rohith
'''
from bulbs.neo4jserver import Graph

class Neo4jDAO(object):
    '''
    This class defines methods for accessing the neo4j database
    All methods for storing and retrieving the nodes and the edges are defined here
    '''
    
    def __init__(self):
        '''
        Constructor - Initialize neo4j database connection
        '''
#        config = Config('http://localhost:7474/db/data/')
        self.g = Graph()
    
    def insert(self,dependency):
        '''
        Method for inserting a parent ,child and their relatedness to database
        '''
        #check whether parent node already exists if not create the node
        parent = self.g.vertices.index.lookup(node=dependency.getParent())
        if(parent==None):
            parent = self.g.vertices.create(node=dependency.getParent())
        else:
            parent = parent.next()
            
        #check whether child node already exists if not create the node
        child = self.g.vertices.index.lookup(node=dependency.getChild())
        if(child==None):
            child = self.g.vertices.create(node=dependency.getChild())
        else:
            child = child.next()
            
        #create edge between parent and child with label "rel" and property "dep"    
        self.g.edges.create(parent, "rel", child, dep=dependency.getRel())
        
        
    