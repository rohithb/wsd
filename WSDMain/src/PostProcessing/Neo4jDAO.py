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
        flag = 0 # to prevent creating duplicate edges
        #check whether parent node already exists if not create the node
        parent = self.g.vertices.index.lookup(node=dependency.getParent())
        if(parent == None):
            parent = self.g.vertices.create(node=dependency.getParent())
        else:
            flag += 1
            parent = parent.next()
            
        #check whether child node already exists if not create the node
        child = self.g.vertices.index.lookup(node=dependency.getChild())
        if(child == None):
            child = self.g.vertices.create(node=dependency.getChild())
        else:
            flag +=1
            child = child.next()
            
        #create edge between parent and child with label "rel" and property "dep"
        if(flag<2):    
            self.g.edges.create(parent, "rel", child, dep=dependency.getRel())
        
    def findDependent(self, word):
        '''
        find the dependent words of param:word and return list of tuple with dependent word and its in-edge weight
        eg : [('business',0.24),('large','0.456').....]
        '''
        dependents =[]
        node = self.g.vertices.index.lookup(node = word)
        if(node == None):
            return None #return None if word not in KB
        node = node.next()
        edges = node.outE()
        if(edges == None):
            return None
        for edge in edges:
            dep = edge.dep
            temp = edge.inV()
            node = temp.node
            dependents.append(tuple([node]+[dep]))
        return dependents
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    