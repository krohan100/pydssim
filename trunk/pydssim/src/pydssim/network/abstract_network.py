from pydssim.util.protected import Protected
from pydssim.util.decorator.require import require
from pydssim.util.decorator.public import public
from pydssim.util.decorator.return_type import return_type
from pydssim.peer.i_peer import IPeer
from sets import ImmutableSet
from multiprocessing import Semaphore
from pydssim.p2p.routing.default_neighbor import DefaultNeighbor
import bisect

class AbstractNetwork(Protected):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self):
       
        self.__simulation = None
        self.__peers = {}
        self.__connectedPeers = []
        self.__disconnectedPeers = []
        self.__advertisedPeers = []
        self.__graph = {}
    
    @public
    def getSimulation(self):
        return self.__simulation
    
    @public
    def setSimulation(self, simulation):
        self.__simulation = simulation
        return self.__simulation
    
    @public
    def countPeers(self):
        return len(self.__peers)
    
    @public
    def addPeer(self, peer):
        if self.__peers.has_key(peer.getPID()):
            raise StandardError()
        self.__peers[peer.getPID()] = peer
        self.__disconnectedPeers.append(peer.getPID())
        return self.__peers[peer.getPID()]
    
    @public
    def removePeer(self, peer):
        if isinstance(peer.getPID(), bool):
            raise TypeError()
        peer = self.__peers[peer.getPID()]
        del self.__peers[peer.getPID()]
        return peer
    
    @public
    @return_type(IPeer)
    @require("id", int)
    def getPeer(self, id):
        if isinstance(id, bool):
            raise TypeError()
        
        return self.__peers[id]
    
    @public
    def getNeighbors(self, peer):
        if not self.__graph.has_key(peer.getPID()):
            return ImmutableSet([])
        return ImmutableSet(self.__graph[peer.getPID()])
    
    @public
    def getGraph(self):
        return self.__graph
    
    @public
    def addNode(self, peer):
        if isinstance(peer.getPID(), bool):
            raise TypeError()
        if self.__graph.has_key(peer.getPID()):
            return True
        sem = Semaphore()
        sem.acquire()
        self.__graph[peer.getPID()] = []
        sem.release()
        return self.__graph.has_key(peer.getPID())
    
    @public
    def removeNode(self, peer):
        if isinstance(peer.getPID(), bool):
            raise TypeError()
        if not self.__graph.has_key(peer.getPID()):
            return False
        sem = Semaphore()
        sem.acquire()
        del self.__graph[peer.getPID()]
        sem.release()
        return not self.__graph.has_key(peer.getPID())
   
    
    @public
    def countNodes(self):
        return len(self.__graph.keys())
    
    @public
    def countConnections(self):
        connections = 0
        for edges in self.__graph.values():
            connections += len(edges)
        return connections
    
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
        if self.__graph.has_key(source.getPID()):
            aux = target in self.__graph[source.getPID()]
        else:
            aux = False
        sem.release()
        return aux
    
    @public
    def createConnection(self, source, target):
       
        if isinstance(source.getPID(), bool) or isinstance(target.getPID(), bool):
            raise TypeError()
        if source == target:
            raise StandardError()
        if (not self.__peers.has_key(source.getPID()) or (not self.__peers.has_key(target.getPID()))):
            raise StandardError()
        if (self.isNeighbor(source, target) == True):
            return True
        if targetId in self.__graph[source.getPID()]:
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