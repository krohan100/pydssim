
from pydssim.util.protected import Protected
from pydssim.network.topology.i_topology import ITopology
from pydssim.util.decorator.public import public

from pydssim.network.i_network import INetwork
from pydssim.peer.peer import Peer
from pydssim.peer.i_peer import IPeer
from pydssim.peer.neighbor.neighbor import Neighbor
from pydssim.peer.neighbor.i_neighbor import INeighbor
from multiprocessing import Semaphore

class Topology(Protected, ITopology):
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
    def setNetwork(self, network):
               
        self.__network = network
        return self.__network

    @public
    def getLayout(self):
        return self.__layout
    
    @public
    def getNetwork(self):
        return self.__network
    tirar neighbor 
    @public
    def addNeighbors(self, source, target):
        
        if (not self.__layout.has_key(source.getId())) and (not self.__layout.has_key(target.getId())) :
            return False
        if source.hasNeighbor(target):
            return False 
        if target.hasNeighbor(source):
            return False   
                   
        semaphore = Semaphore()
        semaphore.acquire()
        source.addNeighbor(target)
        target.addNeighbor(source)
        semaphore.release()
        
        return source.hasNeighbor(target)
        

    @public
    def removeNeighbor(self, source, target):
        
        if (not self.__layout.has_key(source.getId())) and (not self.__layout.has_key(target.getId())) :
            return False
        if source.hasNeighbor(target):
            return False 
        if target.hasNeighbor(source):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        source.removeNeighbor()
        flag = self.__layout[source.getId()].removeNeighbor(self.__layout[source.getId()].getNeighbor(target.getId()))
        semaphore.release()
        
        return flag
        
    @public
    def addPeer(self, peer):
        
        if self.__layout.has_key(peer.getId()):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        
        self.__layout[peer.getId()] = peer
        semaphore.release()
        return self.__layout.has_key(peer.getId())

    @public
    def removePeer(self, peer):
        
        if not self.__layout.has_key(peer.getId()):
            return False
                
        semaphore = Semaphore()
        semaphore.acquire()
        del self.__layout[peer.getId()]
        semaphore.release()
        
        return not self.__layout.has_key(peer.getId())

    @public
    def getPeer(self, peerId):
        
        semaphore = Semaphore()
        semaphore.acquire()
        peer = self.__layout[peerId]
        semaphore.release()
        return peer

    @public
    def getPeers(self):
        semaphore = Semaphore()
        semaphore.acquire()
        peers = self.__layout.itervalues()
        semaphore.release()
        return peers

    @public
    def countPeers(self):
        semaphore = Semaphore()
        semaphore.acquire()
        tamPeers = len(self.__layout)
        semaphore.release()
        return tamPeers
    
    @public
    def getNeighbor(self, source, target):
        
        return self.__layout[source.getId()].getNeighbor(target.getId())
        
    

    @public
    def countNeighbors(self, peer):
                       
        semaphore = Semaphore()
        semaphore.acquire()
        
        count = peer.countNeighbors()
        semaphore.release()
        return count
    
    @public
    def getNeighbors(self, peer):
                
        semaphore = Semaphore()
        semaphore.acquire()
        neighbors = self.__layout[peer.getId()].getNeighbors()
        semaphore.release()
        return neighbors
    
    @public
    def getNeighborIt(self, peer):
                
        semaphore = Semaphore()
        semaphore.acquire()
        neighbors = []
        for neighbor in self.__layout[peer.getId()].getNeighbors():
            neighbors.append(neighbor.getTargetPeer())
        neighborIt = neighbors.__iter__()
        semaphore.release()
        return neighborIt
    
    @public
    def hasPeer(self, peer):
        return self.__layout.has_key(peer.getId())
    
    