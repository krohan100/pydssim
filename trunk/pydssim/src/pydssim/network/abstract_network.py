from pydssim.util.protected import Protected
from pydssim.util.decorator.require import require
from pydssim.util.decorator.public import public
from pydssim.util.decorator.return_type import return_type
from pydssim.peer.i_peer import IPeer
from pydssim.network.topology.topology import Topology
from sets import ImmutableSet
from multiprocessing import Semaphore
from pydssim.p2p.routing.default_neighbor import DefaultNeighbor
import bisect

class AbstractNetwork(Protected):
    """
    Defines the operations of Network .

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self):
       
        self.__simulation = None
        
        self.__connectedPeers = []
        self.__disconnectedPeers = []
        self.__advertisedPeers = []
        self.__topology = Topology(self) 
    
    @public
    def getSimulation(self):
        return self.__simulation
    
    @public
    def setSimulation(self, simulation):
        self.__simulation = simulation
        return self.__simulation
    
    @public
    def countPeers(self):
        return self.__topology.countPeers()
    
    @public
    def addPeer(self, peer):
        return self.__topology.addPeer(peer)
    
    @public
    def removePeer(self, peer):
        
        self.__topology.removePeer(peer)
        
        return peer
    
    @public
    def getPeer(self, id):
        return self.__topology.getPeer(id)
    
    @public
    def getNeighbors(self, peer):
        layout = self.__topology.getLayout()
        if not layout.has_key(peer.getPID()):
            return ImmutableSet([])
        return ImmutableSet(layout[peer.getPID()])
    
     
    @public
    def countPeers(self):
        return len(self.__topology.countPeers())
    
    @public
    def dispatchMessage(self, message):
        sem = Semaphore()
        sem.acquire()
        peer = self.getPeer(message.getTargetId())
        peer.receive(message)
        sem.release()
        return message
    
    @public
    def isNeighbor(self, source, target):
        sem = Semaphore()
        sem.acquire()
        layout = self.__topology.getLayout()
        if layout.has_key(source.getPID()):
            aux = target in layout[source.getPID()]
        else:
            aux = False
        sem.release()
        return aux
    
    @public
    def createConnection(self, source, target):
       
        if source == target:
            raise StandardError()
        layout = self.__topology.getLayout()
        if (not layout.has_key(source.getPID()) or (not layout.has_key(target.getPID()))):
            raise StandardError()
        if (self.isNeighbor(source, target)):
            return True
        if target in layout[source.getPID()]:
            raise StandardError()
        
        sem = Semaphore()
        sem.acquire()
        self.__graph[source.getPID()].append(target)
        self.getPeer(source.getPID()).addNeighbor(DefaultNeighbor(self.getPeer(source.getPID()), target))
        self.__graph[target.getPID()].append(source)
        self.getPeer(target.getPID()).addNeighbor(DefaultNeighbor(self.getPeer(target.getPID()), source))
        sem.release()
        return self.isNeighbor(source, target)
    
    @public
    def removeConnection(self, source, target):
        
        if isinstance(source.getPID(), bool) or isinstance(target.getPID(), bool):
            raise TypeError()
        if source == target:
            raise StandardError()
        if (not self.__peers.has_key(source.getPID())) or (not self.__peers.has_key(target.getPID())):
            raise StandardError()
        if (self.isNeighbor(source, target) == False):
            return False
        
        sem = Semaphore()
        sem.acquire()
        self.__graph[source.getPID()].remove(target)
        if self.__graph.has_key(target.getPID()):
            self.__graph[target.getPID()].remove(source)
        sem.release()
        return not self.isNeighbor(source, target)
    
    @public
    def increaseNumberOfConnectedPeers(self, peer):
        self.__connectedPeers.append(peer)
        self.__disconnectedPeers.remove(peer)
        self.addNode(peer)
        return len(self.__connectedPeers)
    
    @public
    def decreaseNumberOfConnectedPeers(self, peer):
        self.__disconnectedPeers.append(peer)
        self.__connectedPeers.remove(peer)
        self.removeNode(peer)
        return len(self.__connectedPeers)
    
    @public
    def getPeerForConnection(self):
        if len(self.__disconnectedPeers) == 0:
            return None
        return self.__disconnectedPeers[0]
    
    @public
    def getPeerForDisconnection(self):
        if len(self.__connectedPeers) == 0:
            return None
        return self.__connectedPeers[0]
    
    @public
    def countConnectedPeers(self):
        return len(self.__connectedPeers)
    
    @public
    def countDisconnectedPeers(self):
        return len(self.__disconnectedPeers)
    
    @public
    def registerPeerForAdvertisement(self, peer):
        self.__advertisedPeers.append(peer)
        return self.__advertisedPeers[self.__advertisedPeers.index(peer)]
    
    @public
    def getPeerForAdvertisement(self):
        return self.__advertisedPeers[0]
    
    @public
    def unregisterPeerForAdvertisement(self, peer):
        return self.__advertisedPeers.pop(self.__advertisedPeers.index(peer))
    
    @public
    def getConnectedPeers(self):
        return self.__connectedPeers