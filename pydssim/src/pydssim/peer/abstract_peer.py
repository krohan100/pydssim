"""
Defines the module with objective the implementation of AbstractPeer class.

@author: Luiz Gustavo
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 20/08/2009
"""

import hashlib

from twisted.internet import defer

from pydssim.network.protocol.dht.dht_peer import DHTPeer

from pydssim.util.protected import Protected
from pydssim.peer.i_peer import IPeer
from pydssim.util.decorator.public import public, createURN
from pydssim.network.dispatcher.message_dispatcher import MessageDispatcher
from pydssim.peer.repository.service_repository import ServiceRepository
from pydssim.peer.repository.equivalence_repository import EquivalenceRepository
from pydssim.peer.repository.shared_recource_repository import SharedRecourceRepository
from pydssim.peer.repository.history_repository import HistoryRepository
from sets import ImmutableSet
from pydssim.util.logger import Logger
from random import randint
from pydssim.util.resource_maps import *
from pydssim.peer.resource.hardware_resource import Hardware 
from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.peer.resource.service_resource import Service


from random import randint

def createPeer(udpport=4000,ipaddress=None,startport=None):
        
        import sys, os
        
        if ipaddress != None:
            knownPeers = [(ipaddress, startport)]
            
        else:
            knownPeers = None
    
        #print knownPeers, port
        peer = DHTPeer(udpPort=udpport)
        
        #peer.joinNetwork(knownPeers)
        return peer
        

class AbstractPeer(Protected,IPeer):
    
        
    def __init__(self):
        raise NotImplementedError()
    
    
    
    
    def initialize(self,  network,urn, udpPort=4000):
        
        self.__dhtPeer = DHTPeer(udpPort=udpPort) #DHTPeer(udpPort=udpport)createPeer(udpPort)
        self.invalidKeywords = []
        self.keywordSplitters = ['_', '.', '/']
        self.__urn = urn
        self.__pid = self.__dhtPeer.id
        
        self.__network = network
        self.__isConnected = False
        self.__dispatcher = MessageDispatcher(self)
        self.__services = ServiceRepository(self)
        self.__sharedResource = SharedRecourceRepository(self)
        self.__historyResource = HistoryRepository(self)
        self.__equivalences = EquivalenceRepository(self)
        self.__connectionTime = 0
        self.__neighbors = {}
        self.__disconnectionTime = 0
        self.__scheduledDisconnection = False
        
        Logger().resgiterLoggingInfo("Initialize Peer => pid  = %s end URN = %s"%(id,urn))
        
   
    @public
    def getPID(self):
        return self.__pid
    
    @public
    def getDHTPeer(self):
        return self.__dhtPeer
    
    @public
    def getURN(self):
        return self.__urn
    
    @public
    def getType(self):
        return self.__type
    
    
    @public
    def input(self,  data):
        raise NotImplementedError()
    
    @public
    def output(self, data):
        raise NotImplementedError()
    
    '''  rever 
    
    
    
    @public
    def setP2PProtocol(self, protocol):
        self.__protocol = protocol
        self.__protocol.setPeer(self)
        self.__protocol.setP2PTopology(self.__network.getP2PTopology())
        
        for h in self.__protocol.getMessageHandlers():
            self.__dispatcher.registerMessageHandler(h)
            
        return self.__protocol
  


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
    
'''    
   
    
    @public
    def getNetwork(self):
        return self.__network
    
       
    #ve issso
    @public
    def sendMessage(self, message):
        return self.__protocol.sendMessage(message)
    
    
    @public
    def receiveMessage(self, message):
        return self.__protocol.receiveMessage(message)
       
    @public
    def createConnection(self, target):
       
        if self.__network.createConnection(self, target):
            self.addNeighbor(target)
            self.connected()
        return self.isConnected(target)
    
    @public
    def removeConnection(self, target):
        if self.__neighbors.has_key(target.getPID()):
            del self.__neighbors[target.getPID()]
        return not self.isConnected(target)
   
     
    @public
    def getServices(self):
        return self.__services
    
    @public
    def setServices(self, serviceRepository):
        self.__services = serviceRepositoy
        return self.__services
    
    @public
    def loaderServices(self,fileName=None):
        pass
    
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
    def hasNeighbor(self, neighbor):
        return self.__neighbors.has_key(neighbor.getId())
    
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
    def removeNeighbor(self, neighbor):
        ''' coloar mesange de desconectar '''
        if not self.__neighbors.has_key(neighbor.getId()):
            return False
        del self.__neighbors[neighbors.getId()]
        return not self.__neighbors.has_key(neighbors.getId())    
    
    @public
    def countNeighbor(self):
        return len(self.__neighbors)
    
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
    def getHistoryResource(self):    
        return self.__historyResource
    @public
    def getEquivalences(self):
        return self.__equivalences
    
    @public
    def createServices(self,tam=7):
        optionMap   = [ServiceMap(),HardwareMap()]
        optionClass = [Service,Hardware]
       
        
        for i in range(0,randint(1,tam)):
            option = randint(0,1)
            resourceMap = ResourceMap(optionMap[option])
         
            map = resourceMap.Map()
            
            concept = map.keys()[randint(0, len(map.keys()) - 1)]
            resour  = randint(0, (len(map[concept]) - 1))
                    
            service = optionClass[option](pid=createURN("peer"),resource=map[concept][resour])
            self.__services.addElement(service)
        
       
        
   
    '''
   
   
    def createSharedRecource(self):
         for i in range(0,self.getServices().countElements()):
             
            numEle =self.getServices().countElements()
            initial = randint(0, numEle/2 - 1)
            if initial == 0:
                initial =1
            end = randint(numEle/2, numEle - 1)
                  
            ix = 0
            for key in self.getServices().getElements().keys():
                
                if ix < initial:
                    continue
                if ix > end:
                    break 
                
                self.getSharedResource().addElement(self.getServices().getElements()[key])
                
    '''
                
                
                