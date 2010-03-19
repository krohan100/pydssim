'''
Created on 29/01/2010

@author: LGustavo
'''
from random import randint
class Peer():
    
    def __init__( self, id = 0):
        
        self.__neighbor = {}
        self.__id = "127.0.0.1:%s000"%id
        self.__levelNeighbor = 1
        
    def getID(self):
        return self.__id
    
    def getLevelNeighbor(self):
        return self.__levelNeighbor
    
    def getNeighbor(self):
        return self.__neighbor
    
    def setLevelNeighbor(self,level):
        self.__levelNeighbor = level
    
    def addNeighbor(self,id,level=1):
        self.__neighbor[id]= level
    
    def __discoverMinLevel(self):
        
        if max(self.getNeighbor().values())> self.getLevelNeighbor():
            return self.getLevelNeighbor()
        
    def getSuperPeerWithLevel(self,peers,level):
        superPeers = {}
        try:
            superPeers = dict([(peerID,(pLevel,peer)) for peerID, (pLevel,peer) in peers.iteritems() if (pLevel == level and peerID != self.getID())])
            
        except:
            print "erro"
            pass    
        return superPeers
    
    
    def getPeerLevels(self,dportal,peers):
        pass
    
    def discoverNewNeighbor(self,portal,dportal):
        peers = portal.getSuperPeers()
        myLevel = self.getLevelNeighbor()
        print "DP = %s id = %s  l = %s "%(dportal,self.getID(),self.getLevelNeighbor())
        while dportal >= myLevel:
            
            peerLevel =  self.getSuperPeerWithLevel(peers, myLevel)
            auxlevel = myLevel
            while peerLevel == {} and dportal >= auxlevel:
                
                auxlevel+=1
                peerLevel =  self.getSuperPeerWithLevel(peers, auxlevel)
                
            myLevel+=1
            
            if  peerLevel != {}:
                id,(level,peer) = peerLevel.popitem()
            else:
               continue
            
            self.addNeighbor(id, level)
            peer.addNeighbor(self.getID(),level) 
            
            self.setLevelNeighbor(myLevel)
            portal.addSuperPeer(self)
            
            peer.setLevelNeighbor(myLevel)
            portal.addSuperPeer(peer)
            
            print myLevel
             
            print "--->>>", id,level,peer
            print self.getNeighbor()
            
      
        
        
    def discoverNewNeighbor1(self,peers,level=1):
        
        
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
            
            
        