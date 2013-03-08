'''
Created on 08-Mar-2013

@author: rohith
'''
from bulbs.neo4jserver import Graph, Config, NEO4J_URI

class Neo4jDAO(object):
    '''
    This class defines methods for accessing the neo4j database
    All methods for storing and retrieving the nodes and the edges are defined here
    '''
    
    def __init__(self):
        '''
        Constructor - Initialize neo4j database connection
        '''
        config = Config('http://localhost:7474/db/data/')
        self.g = Graph(config)
        
    