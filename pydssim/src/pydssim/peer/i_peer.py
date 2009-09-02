from pydssim.util.interface import Interface

class IPeer(object):
    
    __metaclass__ = Interface
    
    CONTENT_ADVERTISEMENT = 0
    
    def __init__(self):
        raise NotImplementedError()
    
    def getId(self):
        raise NotImplementedError()
    
    def isConnected(self):
        raise NotImplementedError()
    
    def setProtocol(self):
        raise NotImplementedError()
    
    def connect(self, priority):
        raise NotImplementedError()
    
    def disconnect(self, priority):
        raise NotImplementedError()
    
    def connected(self):
        raise NotImplementedError()
    
    def disconnected(self):
        raise NotImplementedError()
    
    def getNetwork(self):
        raise NotImplementedError()
    
    def send(self, message):
        raise NotImplementedError()
    
    def sendMessage(self, message):
        raise NotImplementedError()
    
    def receive(self, message):
        raise NotImplementedError()
    
    def receiveMessage(self, message):
        raise NotImplementedError()
    
    def getMessageDispatcher(self):
        raise NotImplementedError()
    
    def createConnection(self, targetId):
        raise NotImplementedError()
    
    def removeConnection(self, targetId):
        raise NotImplementedError()
    
    def addContent(self, content):
        raise NotImplementedError()
    
    def removeContent(self, id):
        raise NotImplementedError()
    
    def countContents(self):
        raise NotImplementedError()
    
    def getContents(self):
        raise NotImplementedError()
        
    def advertise(self, type):
        raise NotImplementedError()
    
    def setConnectionTime(self, time):
        raise NotImplementedError()
    
    def getConnectionTime(self):
        raise NotImplementedError()
    
    def specifyInterest(self):
        raise NotImplementedError()
    
    def getNeighbor(self, id):
        raise NotImplementedError()
    
    def getNeighbors(self):
        raise NotImplementedError()
    
    def addNeighbor(self, neighbor):
        raise NotImplementedError()
    
    def setDisconnectionTime(self, time):
        raise NotImplementedError()
    
    def getDisconnectionTime(self):
        raise NotImplementedError()
    
    def setScheduledForDisconnection(self, flag):
        raise NotImplementedError()
    
    def getScheduledForDisconnection(self):
        raise NotImplementedError()
    
    # Create grups   
    def createGroups(self):
        raise NotImplementedError()
    
    def getContent(self, id):
        raise NotImplementedError()