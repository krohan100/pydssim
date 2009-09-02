from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from pydssim.network.dispatcher.message_dispatcher import MessageDispatcher
from sets import ImmutableSet
from pydssim.peer.i_peer import IPeer
from random import randint
#from pysocialsim.p2p.message.message_manager import MessageManager

class AbstractPeer(Protected):
    
    CONTENT_ADVERTISEMENT = 0
    
    __public__ = ["CONTENT_ADVERTISEMENT"]
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, id, network):
        self.__id = id
        self.__network = network
        self.__isConnected = False
        self.__dispatcher = MessageDispatcher(self)
        self.__profile = None
        self.__sharedResource = []
        self.__unsharedResource = []
        self.__connectionTime = 0
        self.__neighbors = {}
        self.__disconnectionTime = 0
        self.__scheduledDisconnection = False
        
        
    @public
    def getId(self):
        return self.__id
    
    @public
    def isConnected(self):
        return self.__isConnected
    
    '''
    
    @public
    def setP2PProtocol(self, protocol):
        self.__protocol = protocol
        self.__protocol.setPeer(self)
        self.__protocol.setP2PTopology(self.__network.getP2PTopology())
        
        for h in self.__protocol.getMessageHandlers():
            self.__dispatcher.registerMessageHandler(h)
            
        return self.__protocol
    '''
    
    @public
    def connect(self, priority):
        if self.__isConnected == True:
            return
        self.__protocol.connect(priority)
        self.__connectionTime = priority
        
    
    @public
    def disconnect(self, priority):
        if self.__isConnected == False:
            return
        self.__protocol.disconnect(priority)
    
    @public
    def connected(self):
        if self.__isConnected:
            return True
        self.__isConnected = True
        self.__network.increaseNumberOfConnectedPeers(self.__id)
        return self.__isConnected
    
    @public
    def disconnected(self):
        if not self.__isConnected:
            return
        self.__isConnected = False
        self.__network.decreaseNumberOfConnectedPeers(self.__id)
        return not self.__isConnected
    
    @public
    def getNetwork(self):
        return self.__network
    
    @public
    def send(self, message):
        self.sendMessage(message)
        return message
    
    @public
    def sendMessage(self, message):
        return self.__protocol.sendMessage(message)
    
    @public
    def receive(self, message):
        if self.__id == message.getSourceId():
            return message
        self.receiveMessage(message)
        return message
    
    @public
    def receiveMessage(self, message):
        return self.__protocol.receiveMessage(message)
    
    @public
    def getMessageDispatcher(self):
        return self.__dispatcher
    
    @public
    def createConnection(self, targetId):
        self.__network.createConnection(self.__id, targetId)
        self.connected()
        return self.isConnected()
    
    @public
    def removeConnection(self, targetId):
        self.__network.removeConnection(self.__id, targetId)
        if self.__neighbors.has_key(targetId):
            del self.__neighbors[targetId]
        return not self.isConnected()
   
    @public
    def addResource(self, sharedResource):
        #criar um repositorio de recurosos compartilhados 
        key = resource.getUUID()+resource.getPID()
        if not self.__resources.has_key(key):
            self.__resources[key] = resource
        
        return resource
    
    @public
    def removeResource(self, resource):
        key = resource.getUUID()+resource.getPID()
        if not self.__resources.has_key(key):
            raise StandardError()
        if self.__resources[key] > 0:
            del self.__resources[resources]
            
        return resources
    
    @public
    @return_type(int)
    def countResources(self):
        return len(self.__resources)
    
    @public
    @return_type(dict)
    def getResources(self):
        return self.__resources
    
    
    @public
    def getProfile(self):
        return self.__profile
    
    
    def setProfile(self, profile):
        self.__profile = profile
        return self.__profile
    
    @public
    def advertise(self, type):
        if type == IPeer.CONTENT_ADVERTISEMENT:
            for c in self.__contents.values():
                self.__protocol.advertise(c, type)
    
    @public
    def share(self, type):
        pass
    
    @public
    def setConnectionTime(self, time):
        self.__connectionTime = time
    
    @public
    def getConnectionTime(self):
        return self.__connectionTime
    
    @public
    def specifyInterest(self):
        raise NotImplementedError()
    
    @public
    def getNeighbor(self, id):
        return self.__neighbors[id]
    
    @public
    def getNeighbors(self):
        return ImmutableSet(self.__neighbors.values())    
    
    @public
    def addNeighbor(self, neighbor):
        self.__neighbors[neighbor.getId()] = neighbor
    
    @public    
    def setDisconnectionTime(self, time):
        self.__disconnectionTime = time
    
    @public
    def getDisconnectionTime(self):
        return self.__disconnectionTime
    
    @public
    def setScheduledForDisconnection(self, flag):
        self.__scheduledDisconnection = flag
    
    @public
    def getScheduledForDisconnection(self):
        return self.__scheduledDisconnection
    
    
    
    @public
    def createGroups(self):
        raise NotImplementedError()
        
    '''
    
    @public    
    def getContent(self, id):
        return self.__contents[id]
    
    ''' 
    