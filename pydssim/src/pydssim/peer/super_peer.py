"""
Defines the module with the implementation AbstractPeer class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.util.decorator.public import createURN
from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.logger import Logger

class SuperPeer(AbstractPeer):
    """
    Implements the basic functions of a peer.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self, urn=createURN("peer"),serverPort=4000, maxNeighbor=1):
        
        self.__superPeerNeighbors = {}
        self.__dimension = 1
        
        AbstractPeer.initialize(self, urn,serverPort, maxNeighbor, peerType = AbstractPeer.SUPER)
        
   
    def getDimension(self):
        return self.__dimension
    
    def addSuperPeer(self,peerId,peerLevel=1):
        
        self.addSuperPeerNeighbors(peerId)
        
        
    def addSuperPeerNeighbors(self,peerId):
        self.__superPeerNeighbors[peerId]=peerId
        Logger().resgiterLoggingInfo('Add SuperPeer %s in level : %s' % (peerId, self.getPID()))
        
        
        print "Iam =------->",self.getPID()        
        print "Super peer +>",peerId
        print "SuperPeer neighbors",self.__superPeerNeighbors.keys() 
       
        
        
    def getSuperPeerNeighborsIDs( self ):
    
        """ Return a list of all known peer id's. """
        return self.__superPeerNeighbors.keys()
        
    
        
    def setDimension(self, dimension):
        self.__dimension = dimension

        