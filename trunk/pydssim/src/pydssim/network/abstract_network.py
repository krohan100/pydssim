from pydssim.util.protected import Protected
from pydssim.util.decorator.require import require
from pydssim.util.decorator.public import public
from pydssim.util.decorator.return_type import return_type
from pydssim.peer.i_peer import IPeer
from sets import ImmutableSet
import bisect

class AbstractNetwork(Object):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, topology):
        self.__topology = topology
        self.__topology.setP2PNetwork(self)
        self.__simulation = None
        
        '''
        
        self.__peers = {}
        self.__connectedPeers = []
        self.__disconnectedPeers = []
        self.__advertisedPeers = []
        
        '''
    
    
    colocar essa parte na topologia
    @public
    def getTopology(self):
        return self.__topology
    
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
    def createConnection(self, sourceId, targetId):
        if isinstance(sourceId, bool) or isinstance(targetId, bool):
            raise TypeError()
        if sourceId == targetId:
            raise StandardError()
        if (not self.__peers.has_key(sourceId) or (not self.__peers.has_key(targetId))):
            raise StandardError()
        if (self.__topology.isNeighbor(sourceId, targetId) == True):
            return True
        return self.__topology.createConnection(sourceId, targetId)
    
    @public
    def removeConnection(self, sourceId, targetId):
        if isinstance(sourceId, bool) or isinstance(targetId, bool):
            raise TypeError()
        if sourceId == targetId:
            raise StandardError()
        if (not self.__peers.has_key(sourceId)) or (not self.__peers.has_key(targetId)):
            raise StandardError()
        if (self.__topology.isNeighbor(sourceId, targetId) == False):
            return False
        return self.__topology.removeConnection(sourceId, targetId)
    
    @public
    def increaseNumberOfConnectedPeers(self, peerId):
        self.__connectedPeers.append(peerId)
        self.__disconnectedPeers.remove(peerId)
        return len(self.__connectedPeers)
    
    @public
    def decreaseNumberOfConnectedPeers(self, peerId):
        self.__disconnectedPeers.append(peerId)
        self.__connectedPeers.remove(peerId)
        self.__topology.removeNode(peerId)
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