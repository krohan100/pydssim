from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from pydssim.network.dispatcher.message_dispatcher import MessageDispatcher
from pydssim.peer.repository.service_repository import ServiceRepository
from pydssim.peer.repository.equivalence_repository import EquivalenceRepository
from pydssim.peer.repository.shared_recource_repository import SharedRecourceRepository
from pydssim.peer.repository.unshared_recource_repository import UnSharedRecourceRepository
from sets import ImmutableSet

#from pydssim.peer.i_peer import IPeer
from random import randint
#from pysocialsim.p2p.message.message_manager import MessageManager

class AbstractPeer(Protected):
    
    CONTENT_ADVERTISEMENT = 0
    
    __public__ = ["CONTENT_ADVERTISEMENT"]
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, pid, network):
        self.__pid = pid
        self.__network = network
        self.__isConnected = False
        self.__dispatcher = MessageDispatcher(self)
        self.__services = ServiceRepository(self)
        self.__sharedResource = SharedRecourceRepository(self)
        self.__unSharedResource = UnSharedRecourceRepository(self)
        self.__equivalences = EquivalenceRepository(self)
        self.__connectionTime = 0
        self.__neighbors = {}
        self.__disconnectionTime = 0
        self.__scheduledDisconnection = False
        
        
    @public
    def getPID(self):
        return self.__pid
    
    @public
    def isConnected(self):
        return self.__isConnected
    
    '''  rever 
    
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
        self.__network.increaseNumberOfConnectedPeers(self)
        return self.__isConnected
    
    @public
    def disconnected(self):
        if not self.__isConnected:
            return
        self.__isConnected = False
        self.__network.decreaseNumberOfConnectedPeers(self)
        return not self.__isConnected
    
    @public
    def getNetwork(self):
        return self.__network
    
    @public
    def send(self, message):
        self.sendMessage(message)
        return message
   
    #ve issso
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
    def createConnection(self, target):
       
        if self.__network.createConnection(self, target):
            self.addNeighbor(target)
            self.connected()
        return self.isConnected()
    
    @public
    def removeConnection(self, target):
        if self.__network.removeConnection(self, target):
            if self.__neighbors.has_key(target.getPID()):
                del self.__neighbors[target.getPID()]
        return not self.isConnected()
   
     
    @public
    def getServices(self):
        return self.__services
    
    
    def setServices(self, serviceRepository):
        self.__services = serviceRepositoy
        return self.__services
    
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
    def getNeighbor(self, peerID):
        return self.__neighbors[peerID]
    
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
    def getServices(self):
        return self.__services
        
    @public
    def getSharedResource(self):    
        return self.__sharedResource
    
    @public
    def getUnSharedResource(self):    
        return self.__unSharedResource
    @public
    def getEquivalences(self):
        return self.__equivalences
    
    
    
    @public
    def createGroups(self):
        raise NotImplementedError()
        
    '''
    
    @public    
    def getContent(self, id):
        return self.__contents[id]
    
    ''' 
    