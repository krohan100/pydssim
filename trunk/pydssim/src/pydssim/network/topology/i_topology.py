from pysocialsim.base.interface import Interface

class ITopology(object):
    
    __metaclass__ = Interface
    
    def __init__(self):
        raise NotImplementedError()
    
    def connect(self, peer):
        raise NotImplementedError()
    
    def disconnect(self, peer):
        raise NotImplementedError()
    
    def getNeighbors(self, id):
        raise NotImplementedError()
    
    def setP2PNetwork(self, network):
        raise NotImplementedError()
    
    def getP2PNetwork(self):
        raise NotImplementedError()
    
    def getGraph(self):
        raise NotImplementedError()
    
    def show(self):
        raise NotImplementedError()
    
    def dispatchMessage(self, message):
        raise NotImplementedError()
    
    def createConnection(self, sourceId, targetId):
        raise NotImplementedError()
    
    def removeConnection(self, sourceId, targetId):
        raise NotImplementedError()
    
    def addNode(self, id):
        raise NotImplementedError()
    
    def removeNode(self, id):
        raise NotImplementedError()
    
    def isNeighbor(self, sourceId, targetId):
        raise NotImplementedError()
    
    def countNodes(self):
        raise NotImplementedError()
    
    def countConnections(self):
        raise NotImplementedError()