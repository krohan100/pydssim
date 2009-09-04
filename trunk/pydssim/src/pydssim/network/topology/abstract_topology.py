from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from sets import ImmutableSet
from multiprocessing import Semaphore
from pydssim.p2p.routing.default_neighbor import DefaultNeighbor

class AbstractTopology(Protected):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self):
        self.__network = None
 sds       self.__graph = {}
    
    @public
    def setNetwork(self, network):
        self.__network = network
        return self.__network
    
    @public
    def connect(self, peer):
        raise NotImplementedError()
    
    @public
    def disconnect(self, peer):
        raise NotImplementedError()
    
    @public
    def getNeighbors(self, id):
        if not self.__graph.has_key(id):
            return ImmutableSet([])
        return ImmutableSet(self.__graph[id])
    
    @public
    def getNetwork(self):
        return self.__network
    
    @public
    def getGraph(self):
        return self.__graph
    
    @public
    def show(self):
        raise NotImplementedError()

    @public
    def dispatchMessage(self, message):
        sem = Semaphore()
        sem.acquire()
        peer = self.getNetwork().getPeer(message.getTargetId())
        peer.receive(message)
        sem.release()
        return message
    
    @public
    def createConnection(self, sourceId, targetId):
        if isinstance(sourceId, bool) or isinstance(targetId, bool):
            raise TypeError()
        if targetId in self.__graph[sourceId]:
            raise StandardError()
        sem = Semaphore()
        sem.acquire()
        self.__graph[sourceId].append(targetId)
        self.__network.getPeer(sourceId).addNeighbor(DefaultNeighbor(self.__network.getPeer(sourceId), targetId))
        self.__graph[targetId].append(sourceId)
        self.__network.getPeer(targetId).addNeighbor(DefaultNeighbor(self.__network.getPeer(targetId), sourceId))
        sem.release()
        return self.isNeighbor(sourceId, targetId)
    
    @public
    def removeConnection(self, sourceId, targetId):
        if isinstance(sourceId, bool) or isinstance(targetId, bool):
            raise TypeError()
        if not self.isNeighbor(sourceId, targetId):
            return True
        sem = Semaphore()
        sem.acquire()
        self.__graph[sourceId].remove(targetId)
        if self.__graph.has_key(targetId):
            self.__graph[targetId].remove(sourceId)
        sem.release()
        return not self.isNeighbor(sourceId, targetId)
    
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
    def countNodes(self):
        return len(self.__graph.keys())
    
    @public
    def countConnections(self):
        connections = 0
        for edges in self.__graph.values():
            connections += len(edges)
        return connections
    
