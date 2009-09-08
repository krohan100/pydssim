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
        if self.__peers.has_key(peer.getId()):
            raise StandardError()
        self.__peers[peer.getId()] = peer
        self.__disconnectedPeers.append(peer.getId())
        return self.__peers[peer.getId()]
    
    @public
    def removePeer(self, id):
        if isinstance(id, bool):
            raise TypeError()
        peer = self.__peers[id]
        del self.__peers[id]
        return peer
    
    @public
    @return_type(IPeer)
    @require("id", int)
    def getPeer(self, id):
        if isinstance(id, bool):
            raise TypeError()
        
        return self.__peers[id]
    
    @public
    def getNeighbors(self, id):
        if not self.__graph.has_key(id):
            return ImmutableSet([])
        return ImmutableSet(self.__graph[id])
    
    @public
    def getGraph(self):
        return self.__graph
    
    @public
    def addNode(self, id):
        if isinstance(id, bool):
            raise TypeError()
        if self.__graph.has_key(id):
            return True
        sem = Semaphore()
        sem.acquire()
        self.__graph[id] = []
        sem.release()
        return self.__graph.has_key(id)
    
    @public
    def removeNode(self, id):
        if isinstance(id, bool):
            raise TypeError()
        if not self.__graph.has_key(id):
            return False
        sem = Semaphore()
        sem.acquire()
        del self.__graph[id]
        sem.release()
        return not self.__graph.has_key(id)
   
    
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
    def isNeighbor(self, sourceId, targetId):
        sem = Semaphore()
        sem.acquire()
        if self.__graph.has_key(sourceId):
            aux = targetId in self.__graph[sourceId]
        else:
            aux = False
        sem.release()
        return aux
    
    @public
    def createConnection(self, sourceId, targetId):
       
        if isinstance(sourceId, bool) or isinstance(targetId, bool):
            raise TypeError()
        if sourceId == targetId:
            raise StandardError()
        if (not self.__peers.has_key(sourceId) or (not self.__peers.has_key(targetId))):
            raise StandardError()
        if (self.isNeighbor(sourceId, targetId) == True):
            return True
        if targetId in self.__graph[sourceId]:
            raise StandardError()
        
        sem = Semaphore()
        sem.acquire()
        self.__graph[sourceId].append(targetId)
        self.getPeer(sourceId).addNeighbor(DefaultNeighbor(self.getPeer(sourceId), targetId))
        self.__graph[targetId].append(sourceId)
        self.getPeer(targetId).addNeighbor(DefaultNeighbor(self.getPeer(targetId), sourceId))
        sem.release()
        return self.isNeighbor(sourceId, targetId)
    
    @public
    def removeConnection(self, sourceId, targetId):
        
        if isinstance(sourceId, bool) or isinstance(targetId, bool):
            raise TypeError()
        if sourceId == targetId:
            raise StandardError()
        if (not self.__peers.has_key(sourceId)) or (not self.__peers.has_key(targetId)):
            raise StandardError()
        if (self.isNeighbor(sourceId, targetId) == False):
            return False
        
        sem = Semaphore()
        sem.acquire()
        self.__graph[sourceId].remove(targetId)
        if self.__graph.has_key(targetId):
            self.__graph[targetId].remove(sourceId)
        sem.release()
        return not self.isNeighbor(sourceId, targetId)
    
    @public
    def increaseNumberOfConnectedPeers(self, peerId):
        self.__connectedPeers.append(peerId)
        self.__disconnectedPeers.remove(peerId)
        self.addNode(peerId)
        return len(self.__connectedPeers)
    
    @public
    def decreaseNumberOfConnectedPeers(self, peerId):
        self.__disconnectedPeers.append(peerId)
        self.__connectedPeers.remove(peerId)
        self.removeNode(peerId)
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
    def registerPeerForAdvertisement(self, id):
        self.__advertisedPeers.append(id)
        return self.__advertisedPeers[self.__advertisedPeers.index(id)]
    
    @public
    def getPeerForAdvertisement(self):
        return self.__advertisedPeers[0]
    
    @public
    def unregisterPeerForAdvertisement(self, id):
        return self.__advertisedPeers.pop(self.__advertisedPeers.index(id))
    
    @public
    def getConnectedPeers(self):
        return self.__connectedPeers