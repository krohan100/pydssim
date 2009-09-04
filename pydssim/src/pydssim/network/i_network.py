from pysocialsim.base.interface import Interface

class IP2PNetwork(object):
    
    __metaclass__ = Interface
    
    def __init__(self):
        raise NotImplementedError()
    
    def getP2PTopology(self):
        raise NotImplementedError()
    
    def getSimulation(self):
        raise NotImplementedError()
    
    def setSimulation(self, simulation):
        raise NotImplementedError()
    
    def countPeers(self):
        raise NotImplementedError()
    
    def addPeer(self, peer):
        raise NotImplementedError()
    
    def removePeer(self, id):
        raise NotImplementedError()
    
    def getPeer(self, id):
        raise NotImplementedError()
    
    def createConnection(self, sourceId, targetId):
        raise NotImplementedError()
    
    def removeConnection(self, sourceId, targetId):
        raise NotImplementedError()
    
    def increaseNumberOfConnectedPeers(self, peerId):
        raise NotImplementedError()
    
    def decreaseNumberOfConnectedPeers(self, peerId):
        raise NotImplementedError()
    
    def getPeerForConnection(self):
        raise NotImplementedError()
    
    def getPeerForDisconnection(self):
        raise NotImplementedError()
    
    def countConnectedPeers(self):
        raise NotImplementedError()
    
    def countDisconnectedPeers(self):
        raise NotImplementedError()
    
    def getPeerForAdvertisement(self):
        raise NotImplementedError()
    
    def registerPeerForAdvertisement(self, id):
        raise NotImplementedError()
    
    def unregisterPeerForAdvertisement(self, id):
        raise NotImplementedError()
    
    def getConnectedPeers(self):
        raise NotImplementedError()