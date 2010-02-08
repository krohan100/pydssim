'''
Created on 29/01/2010

@author: LGustavo
'''
from random import randint
import math

class Portal:
    
    def __init__( self):
        
        self.__superPeers = {}
        
        self.__dimension = 1
    
    def getSuperPeers(self):
        return self.__superPeers
    
           
    def getDimension(self):
        return self.__dimension
    
    def updatePeerLevel(self,peerId,peerLevel): 
        self.__superPeers[peerId]=peerLevel
           
    def addSuperPeer(self,peerId,peerLevel):
        host,port = peerId.split(":")
        self.__superPeers[peerId]=(peerLevel,host,port)
        
        
        if math.log(len(self.__superPeers),2) > self.__dimension:
            self.__dimension = int(math.log(len(self.__superPeers),2))+1
          
    
    def getSuperPeerWithLevel(self,level):
        superPeers = {}
        try:
            superPeers = dict([(pID,pLevel) for pID, pLevel in self.getSuperPeers().iteritems() if pLevel == level])
        except:
            pass    
        return superPeers
    
    def getSuperPeerWithLevelMin(self):
        superPeers = {}
        
        try:
            mini = min(self.getSuperPeers().values())
            superPeers = dict([(pID,pLevel) for pID, pLevel in self.getSuperPeers().iteritems() if pLevel == mini])
        except:
            pass    
        return superPeers
            
       
        
        
        
    
        