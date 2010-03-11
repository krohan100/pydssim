"""
Defines the module with the implementation AbstractPeer class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.util.decorator.public import public,createURN
from pydssim.util.logger import Logger
from random import randint
import math

class PortalPeer(AbstractPeer):
    """
    Implements the basic functions of a peer.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self,network, urn=createURN("peer"),serverPort=4000):
        
        AbstractPeer.initialize(self,  network,urn,serverPort,network.getMaxNeighbor(),peerType = AbstractPeer.PORTAL)
        self.__superPeers = {}
        
        self.__dimension = 1
    
    def getSuperPeers(self):
        return self.__superPeers
    
    def numberOfSuperPeers( self ):
   
        """ Return the number of known peer's. """
        return len(self.getSuperPeers()) 
    
    def getSuperPeerIDs( self ):
    
        """ Return a list of all known peer id's. """
        return self.getSuperPeers().keys()      
    
    def getDimension(self):
        return self.__dimension
    
    def updatePeerLevel(self,peerId,peerLevel): 
        self.__superPeers[peerId]=peerLevel
           
    def addSuperPeer(self,peerId,peerLevel=1):
        self.__superPeers[peerId]=peerLevel
        Logger().resgiterLoggingInfo('Add Super Peer %s in level : %s' % (peerId, peerLevel))
        ###
        #fazer o al do hyper
        
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
    
    

        