
from pydssim.util.protected import Protected
from pydssim.network.topology.i_topology import ITopology
from pydssim.util.decorator.public import public

from pydssim.network.i_network import INetwork
from pydssim.peer.peer import Peer
from pydssim.peer.i_peer import IPeer
from pydssim.peer.neighbor.neighbor import Neighbor
from pydssim.peer.neighbor.i_neighbor import INeighbor
from multiprocessing import Semaphore

class AbstractTopology(Protected, ITopology):
    """
    Defines the operations of Network topology.

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self,network=None):
        self.initialize(network)

    def initialize(self,network):
        self.__layout = {}
        self.__network = network
    
    @public
    def setNetwork(self, peerToPeerNetwork):
               
        self.__peerToPeerNetwork = peerToPeerNetwork
        return self.__peerToPeerNetwork

    @public
    def getNetwork(self):
        return self.__peerToPeerNetwork
    
    @public
    def addNeighbor(self, source, target):
                
        semaphore = Semaphore()
        semaphore.acquire()
        peer = self.__layout[source.getId()]
        if peer.hasNeighbor(target):
            return False
        targetPeer = self.__layout[target.getId()]
        neighbor = Neighbor(targetPeer)
        peer.addNeighbor(neighbor)
        semaphore.release()
        return peer.hasNeighbor(target)
        
parei aui

    @public
    def removeNeighbor(self, sourceId, targetId):
        requires(sourceId, int)
        requires(targetId, int)
        
        pre_condition(sourceId, lambda x: x > 0)
        pre_condition(targetId, lambda x: x > 0)
        pre_condition(sourceId, lambda x: x <> None)
        pre_condition(targetId, lambda x: x <> None)
        pre_condition(sourceId, lambda x: self.__layout.has_key(sourceId))
        pre_condition(targetId, lambda x: self.__layout[sourceId].hasNeighbor(x))
        
        semaphore = Semaphore()
        semaphore.acquire()
        rtrn = returns(self.__layout[sourceId].removeNeighbor(self.__layout[sourceId].getNeighbor(targetId)), bool)
        semaphore.release()
        return rtrn
        
    @public
    def addPeer(self, PeerId):
        requires(PeerId, int)
        
        pre_condition(PeerId, lambda x: x > 0)
        pre_condition(PeerId, lambda x: x <> None)
        
        semaphore = Semaphore()
        semaphore.acquire()
        if self.__layout.has_key(PeerId):
            return False
        Peer = Peer(PeerId, self)
        self.__layout[Peer.getId()] = Peer
        semaphore.release()
        return returns(self.__layout.has_key(Peer.getId()), bool)

    @public
    def removePeer(self, PeerId):
        requires(PeerId, int)
        
        pre_condition(PeerId, lambda x: x > 0)
        pre_condition(PeerId, lambda x: x <> None)
        
        semaphore = Semaphore()
        semaphore.acquire()
        if not self.__layout.has_key(PeerId):
            return False
        
        del self.__layout[PeerId]
        semaphore.release()
        return returns(not self.__layout.has_key(PeerId), bool)

    @public
    def getPeer(self, PeerId):
        requires(PeerId, int)
        
        pre_condition(PeerId, lambda x: x > 0)
        pre_condition(PeerId, lambda x: x <> None)
        pre_condition(PeerId, lambda x: self.__layout.has_key(PeerId))
        
        semaphore = Semaphore()
        semaphore.acquire()
        rtnr = returns(self.__layout[PeerId], IPeer)
        semaphore.release()
        return rtnr

    @public
    def getPeers(self):
        semaphore = Semaphore()
        semaphore.acquire()
        rtrn = self.__layout.itervalues()
        semaphore.release()
        return rtrn

    @public
    def countPeers(self):
        semaphore = Semaphore()
        semaphore.acquire()
        rtrn = returns(len(self.__layout), int)
        semaphore.release()
        return rtrn
    @public
    def getNeighbor(self, sourceId, targetId):
        requires(sourceId, int)
        requires(targetId, int)
        
        pre_condition(sourceId, lambda x: x > 0)
        pre_condition(targetId, lambda x: x > 0)
        pre_condition(sourceId, lambda x: x <> None)
        pre_condition(targetId, lambda x: x <> None)
        pre_condition(sourceId, lambda x: self.__layout.has_key(x))
        pre_condition(targetId, lambda x: self.__layout[sourceId].hasNeighbor(x))
        
        semaphore = Semaphore()
        semaphore.acquire()
        rtrn = returns(self.__layout[sourceId].getNeighbor(targetId), INeighbor)
        semaphore.release()
        return rtrn
    
    @public
    def getNeighbors(self, PeerId):
        requires(PeerId, int)
        
        pre_condition(PeerId, lambda x: x > 0)
        pre_condition(PeerId, lambda x: x <> None)
        pre_condition(PeerId, lambda x: self.__layout.has_key(x))
        
        semaphore = Semaphore()
        semaphore.acquire()
        rtrn = self.__layout[PeerId].getNeighbors()
        semaphore.release()
        return rtrn

    @public
    def countNeighbors(self, PeerId):
        requires(PeerId, int)
        
        pre_condition(PeerId, lambda x: x > 0)
        pre_condition(PeerId, lambda x: x <> None)
        pre_condition(PeerId, lambda x: self.__layout.has_key(PeerId))
        
        semaphore = Semaphore()
        semaphore.acquire()
        Peer = self.__layout[PeerId]
        rtrn = returns(Peer.countNeighbors(), int)
        semaphore.release()
        return rtrn
    
    @public
    def getNeighbors(self, PeerId):
        requires(PeerId, int)
        
        pre_condition(PeerId, lambda x: x > 0)
        pre_condition(PeerId, lambda x: x <> None)
        pre_condition(PeerId, lambda x: self.__layout.has_key(PeerId))
        
        semaphore = Semaphore()
        semaphore.acquire()
        neighbors = []
        for Neighbor in self.__layout[PeerId].getNeighbors():
            neighbors.append(Neighbor.getTargetPeer())
        rtrn = neighbors.__iter__()
        semaphore.release()
        return rtrn
    
    @public
    def hasPeer(self, PeerId):
        return returns(self.__layout.has_key(PeerId), bool)
    
    @public
    def hasNeighbor(self):
        raise NotImplementedError()