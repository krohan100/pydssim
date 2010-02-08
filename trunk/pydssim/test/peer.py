'''
Created on 29/01/2010

@author: LGustavo
'''
from random import randint
class Peer():
    
    def __init__( self, id = 0):
        
        self.__neighbor = {}
        self.__id = "127.0.0.1:%s"%id
        self.__levelNeighbor = randint(1,5)#1
        
    def getID(self):
        return self.__id
    
    def getLevelNeighbor(self):
        return self.__levelNeighbor
    
    def getNeighbor(self):
        return self.__Neighbor
    
    def setLevelNeighbor(self,level):
        self.__levelNeighbor = level
    
    def addNeighbor(self,id,level=1):
        self.__neighbor[id]= level
    
    def __discoverMinLevel(self):
        
        if max(self.getNeighbor().values())> self.getLevelNeighbor():
            return self.getLevelNeighbor()
        
        
    def discoverNewNeighbor(self,peers,level=1):
        
        
        for idKey,npeer in peers.iteritems():
            if idKey in self.__neighbor:
                return False
            if npeer.getLevelNeighbor() == self.__levelNeighbor:
                self.addNeighbor(npeer.getID(), self.__levelNeighbor)
                npeer.addNeighbor(self.getID(),self.__levelNeighbor)
                self.setLevelNeighbor(self.getLevelNeighbor()+1)
                npeer.setLevelNeighbor(max(self.getNeighbor().values()))
                return True
        
        for idKey,npeer in peers.iteritems():
            pass   
            
            
        