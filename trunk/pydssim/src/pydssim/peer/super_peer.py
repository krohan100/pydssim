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

    def __init__(self,network, urn=createURN("peer"),serverPort=4000):
        
        AbstractPeer.initialize(self, network,urn,serverPort,network.getMaxNeighbor(), peerType = AbstractPeer.SUPER)
        
        self.__superPeerNeighbors = {}
        
    def newSuperPeer(self,portalID):
        
        host,port = portalID.split(":")
        resp = self.connectAndSend(host, port, AbstractMessageHandler.INSERTSPEER, 
                        '%s %s %d' % (self.getPID(),
                                  self.getServerHost(), 
                                  self.getServerPort()))#[0]
        Logger().resgiterLoggingInfo ("Insert SuperPeers (%s,%s)" % (self.getServerHost(),self.getServerPort()))
        self.setMySuperPeer(self.getPID())
        self.setPeerType(AbstractPeer.SUPER)
        
    

        