"""
Defines the module with objective the implementation of AbstractPeer class.

@author: Luiz Gustavo
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 20/08/2009
"""

import socket
import struct
import threading
import time
import traceback

from pydssim.util.decorator.public import createURN
from pydssim.network.dispatcher.message_dispatcher import MessageDispatcher
from pydssim.peer.repository.service_repository import ServiceRepository
from pydssim.peer.repository.equivalence_repository import EquivalenceRepository
from pydssim.peer.repository.shared_recource_repository import SharedRecourceRepository
from pydssim.peer.repository.history_repository import HistoryRepository

from pydssim.peer.trust.trust_manager import TrustManager
#from sets import ImmutableSet
from pydssim.util.logger import Logger
from random import randint
from pydssim.util.resource_maps import *
from pydssim.peer.resource.hardware_resource import Hardware 
from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.peer.resource.service_resource import Service
from pydssim.network.dispatcher.message_handler_insert import MessageHandlerInsertPeer
from pydssim.network.dispatcher.message_handler_list_peer import MessageHandlerListPeer
from pydssim.network.dispatcher.message_handler_peer_exit import MessageHandlerPeerExit
from pydssim.network.dispatcher.message_handler_peer_name import MessageHandlerPeerName
from pydssim.network.dispatcher.message_handler_super_peer import MessageHandlerSuperPeer
from pydssim.network.dispatcher.message_handler_insert_super_peer import MessageHandlerInsertSuperPeer
from pydssim.network.dispatcher.message_handler_list_super_peer import MessageHandlerListSuperPeer
from pydssim.network.dispatcher.message_handler_update_level import MessageHandlerUpdatePeerLevel

from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.peer.peer_connection import PeerConnection


from random import randint


class AbstractPeer:
    
    NUMBER = 3
    SUPER  = "SUPER_PEER"
    SIMPLE = "SIMPLE_PEER"
    PORTAL = "PORTAL_PEER"
    NULL   = "NULL"
    
        
    def __init__(self):
        raise NotImplementedError()
    
    def __createHandleMessage(self):
        
        dispatcher = MessageDispatcher(self)
        dispatcher.registerMessageHandler(MessageHandlerInsertPeer(self))
        dispatcher.registerMessageHandler(MessageHandlerListPeer(self))
        dispatcher.registerMessageHandler(MessageHandlerPeerExit(self))
        dispatcher.registerMessageHandler(MessageHandlerPeerName(self))
        dispatcher.registerMessageHandler(MessageHandlerSuperPeer(self))
        dispatcher.registerMessageHandler(MessageHandlerInsertSuperPeer(self))
        dispatcher.registerMessageHandler(MessageHandlerListSuperPeer(self))
        dispatcher.registerMessageHandler(MessageHandlerUpdatePeerLevel(self))
       
        
        
        
        return dispatcher
    
    def initialize(self,  urn=createURN("peer"), serverPort=3000, maxPeers=1,  peerType = SIMPLE):
        import socket
        
        self.__peerType = peerType
        
        self.__maxPeers = int(maxPeers)
        self.__serverPort = int(serverPort)
        self.__attemptedConnectionNumber = 0
        self.__serverHost = socket.gethostbyname(socket.gethostname())
        self.__pid = '%s:%d' % (self.__serverHost, self.__serverPort)
        self.__peerLock = threading.Lock()
        self.__peerNeighbors = {}     
        self.__shutdown = False  
    
        self.__handlers = {}
        self.__router = None
        
        self.__urn = urn
              
        self.__isConnected = False
        self.__logger = Logger('w','logging_simulation_peer.log')
        self.__logger.resgiterLoggingInfo("Initialize Peer =>  URN = %s, IP = %s port = %s"%(self.__urn,self.__serverHost,self.__serverPort))
        self.__dispatcher = self.__createHandleMessage()
        
        self.__services = ServiceRepository(self)
        self.__trustManager = TrustManager(self)
       
        self.__sharedResource = SharedRecourceRepository(self)
        self.__historyResource = HistoryRepository(self)
        self.__equivalences = EquivalenceRepository(self)
        #self.__trust = 
        
        self.__connectionTime = 0
        
        self.__disconnectionTime = 0
        self.__scheduledDisconnection = False
        
         
    def __handlePeer( self, clientSock ):
    
        """
        handlepeer( new socket connection ) -> ()
    
        Dispatches messages from the socket connection
        """
    
        Logger().resgiterLoggingInfo('New child ' + str(threading.currentThread().getName())) 
        Logger().resgiterLoggingInfo('Connected ' + str(clientSock.getpeername()))
    
        host, port = clientSock.getpeername()
        peerConn = PeerConnection( None, host, port, clientSock)
        
        try:
            msgType, msgData = peerConn.recvData()
            
            if msgType: 
                msgType = msgType.upper()
                
            if not self.__dispatcher.hasTypeMessage(msgType):   
            #if msgType not in self.__dispatcher.getMessageHandlers():
                Logger().resgiterLoggingInfo('Not handled: %s: %s' % (msgType, msgData))
            else:
                Logger().resgiterLoggingInfo('Handling peer msg: %s: %s' % (msgType, msgData))
                self.__dispatcher.executeHandleMessage(msgType, peerConn, msgData)
                #self.__dispatcher.getMessageHandlers()[ msgType ].e( peerConn, msgData )
        except KeyboardInterrupt:
            raise
        except:
            
            traceback.print_exc()
        
        Logger().resgiterLoggingInfo('Disconnecting ' + str(clientSock.getpeername())) 
        peerConn.close()
        
    
    def mainLoop( self ):
    
        s = self.makeServerSocket( self.getServerPort() )
        s.settimeout(2)
        Logger().resgiterLoggingInfo('Server started: %s (%s:%d)'  % ( self.getPID(), self.getServerHost(), self.getServerPort() ))
        
        
        while not self.getShutdown():
            #print "Server started: %s (%s:%d)"%(self.myID, self.serverHost, self.serverPort)
            try:
                #print ('Listening for connections port %s'%self.getServerPort() )
               
                clientSock, clientAddr = s.accept()
                clientSock.settimeout(None)
        
                t = threading.Thread( target = self.__handlePeer,
                              args = [ clientSock ] )
                t.start()
                
            except KeyboardInterrupt:
                print 'KeyboardInterrupt: stopping mainloop'
                self.getShutdown = True
                continue
            except:
            
                #traceback.print_exc()
                continue
    
        
        print 'Main loop exiting' 
    
        s.close()
        
    def getShutdown(self):
        return self.__shutdown
    
    def getRouter(self):
        return self.__router
    
    def getAttemptedConnectionNumber(self):
        return self.__attemptedConnectionNumber
    
    def setAttemptedConnectionNumber(num):
        self.__attemptedConnectionNumber = num
           
        
    def getMySuperPeer(self):
        return self.__mySuperPeer
    
    def setMySuperPeer(self,super):
        
        self.__mySuperPeer = super
    
    def getServerHost(self):
        return self.__serverHost
    
    def getServerPort(self):
        return self.__serverPort
    
    def getPeerLock(self):
        return self.__peerLock
   
    def getMaxPeers(self):
        return self.__maxPeers
    
    def getPeerType(self):
        return self.__peerType
    
    def setPeerType(self,type):
        
        self.__peerType = type
        
    def getPID(self):
        return self.__pid
    
   
    def getPort(self):
        return self.__port
    
      
    def getURN(self):
        return self.__urn
    
    
    def getType(self):
        return self.__type
    
    def __runstabilizer( self, stabilizer, delay ):
    
        while not self.__shutdown:
            stabilizer()
            time.sleep( delay )

      
    def setPID( self, myID ):
    
           self.__pid = myID

  
    def startStabilizer( self, stabilizer, delay ):
    
        """ Registers and starts a stabilizer function with this peer. 
        The function will be activated every <delay> seconds. 
    
        """
        t = threading.Thread( target = self.__runstabilizer, 
                      args = [ stabilizer, delay ] )
        t.start()

    def addRouter( self, router ):
    
       
        self.__router = router

  
    


    def makeServerSocket( self, port, backlog=5 ):
  
        """ Constructs and prepares a server socket listening on the given 
        port.
    
        """
        s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        s.bind( ( '', port ) )
        s.listen( backlog )
        return s


    def sendToPeer( self, peerID, msgType, msgData, waitreply=True ):
   
        """
        sendtopeer( peer id, message type, message data, wait for a reply )
         -> [ ( reply type, reply data ), ... ] 
    
        Send a message to the identified peer. In order to decide how to
        send the message, the router handler for this peer will be called.
        If no router function has been registered, it will not work. The
        router function should provide the next immediate peer to whom the 
        message should be forwarded. The peer's reply, if it is expected, 
        will be returned.
    
        Returns None if the message could not be routed.
        """
    
        if self.__router:
            nextpid, host, port = self.__router( peerID )
        if not self.__router or not nextpid:
            Logger().resgiterLoggingInfo('Unable to route %s to %s' % (msgType, peerID))
            return None
        #host,port = self.peers[nextpid]
        return self.connectAndSend( host, port, msgType, msgData,
                        pid=nextpid,
                        waitreply=waitreply )
    


   
    def connectAndSend( self, host, port, msgType, msgData, 
            pid=None, waitreply=True ):
   
        msgreply = []
        num = self.getAttemptedConnectionNumber()
        
        while  num != AbstractPeer.NUMBER:
            
            Logger().resgiterLoggingInfo("ConnectAndSend peers from (%s,%s) %s number %d" % (host,port,msgType,num))
            
            try:
                peerConn = PeerConnection( pid, host, port)
                peerConn.sendData( msgType, msgData )
                if waitreply:
                    onereply = peerConn.recvData()
                    while (onereply != (None,None)):
                        msgreply.append( onereply )
                        Logger().resgiterLoggingInfo('Got reply %s: %s' % ( pid, str(msgreply) ))
                        onereply = peerConn.recvData()
                peerConn.close()
                break
            except KeyboardInterrupt:
                raise
            except:
                num += 1
                Logger().resgiterLoggingInfo("Erro de Connecao peers from (%s,%s) %s %d" % (host,port,msgType, num))
        
        if num == AbstractPeer.NUMBER:
            self.setMySuperPeer(self.getPID())
            self.setPeerType(AbstractPeer.SUPER)
            
        return msgreply
    '''

    def connectSuperPeer(self,portalID):
        
        """ buildpeers(host, port, hops) 
    
        Attempt to build the local peer list up to the limit stored by
        self.maxPeers, using a simple depth-first search given an
        initial host and port as starting point. The depth of the
        search is limited by the hops parameter.
    
        """
       
        host,port = portalID.split(":")    
        Logger().resgiterLoggingInfo ("Building Super peers from (%s,%s)" % (host,port))
         
    
        try:
            #print "contacting " #+ peerID
            _, peerID = self.connectAndSend(host, port, AbstractMessageHandler.PEERNAME, '')[0]
    
            #print "contacted " + peerID
            resp = self.connectAndSend(host, port, AbstractMessageHandler.INSERTPEER, 
                        '%s %s %s %d' % (self.getPID(),self.getMySuperPeer(),
                                  self.getServerHost(), 
                                  self.getServerPort()))#[0]
           
            
            if (resp[0][0] != AbstractMessageHandler.REPLY) or (peerID in self.getPeerIDs()):
                return
            
                      
            self.addPeerNeighbor(peerID, host, port,resp[1][1])
            
            
        except:
            traceback.print_exc()
            #print "eerrroooo" 
            self.removePeer(peerID)
            
    ''' 
    
     
    def connectPortal(self, portalID, hops=1,type=SIMPLE):
    
        """ ConnectPeers(host, port, hops) 
    
        Attempt to build the local peer list up to the limit stored by
        self.maxPeers, using a simple depth-first search given an
        initial host and port as starting point. The depth of the
        search is limited by the hops parameter.
    
        """
        
    
        peerID = None
        
        host,port = portalID.split(":")
    
        Logger().resgiterLoggingInfo ("Connecting to PortalPeers (%s,%s)" % (host,port))
        
        try:
            #print "contacting " #+ peerID
            _, peerID = self.connectAndSend(host, port, AbstractMessageHandler.PEERNAME, '')[0]
    
           
            # do recursive depth first search to add more peers
            resp = self.connectAndSend(host, port, AbstractMessageHandler.LISTSPEERS, '',
                        pid=peerID)
            
            
            
            if len(resp) > 1:
                resp.reverse()
            resp.pop()    # get rid of header count reply
            
            super = True
            while len(resp):
                
                
                nextpid,level,dimension = resp.pop()[1].split()
                
                if nextpid != self.getPID():
                    hostSuper,portSuper = nextpid.split(":")
                    if self.connectSuperPeers(hostSuper, portSuper, hops,type ):
                        Logger().resgiterLoggingInfo ("Connected to SUperPeers (%s,%s)" % (host,port))
                        
                        super = False
                        if type == AbstractPeer.SIMPLE:
                            break
                        self.addSuperPeerNeighbors(nextpid)
            
            if super:
                Logger().resgiterLoggingInfo ("sem super")
                #self.__newSuperPeer(host, port)       
                
        except:
            traceback.print_exc()
            #print "eerrroooo" 
            self.removePeer(peerID)       
    
    
    
    def connectSuperPeers(self, host, port, hops=1,type=SIMPLE):
    
        """ ConnectPeers(host, port, hops) 
    
        Attempt to build the local peer list up to the limit stored by
        self.maxPeers, using a simple depth-first search given an
        initial host and port as starting point. The depth of the
        search is limited by the hops parameter.
    
        """
        if self.maxPeersReached() or not hops:
            return
    
        peerID = None
    
        Logger().resgiterLoggingInfo ("Connecting to SuperPeers (%s,%s)" % (host,port))
        
        try:
            #print "contacting " #+ peerID
            _, peerID = self.connectAndSend(host, port, AbstractMessageHandler.PEERNAME, '')[0]
    
            #print "contacted " + peerID
            
            if type == AbstractPeer.SIMPLE:
                msgHandler = AbstractMessageHandler.INSERTPEER
                
            else:
                msgHandler = AbstractMessageHandler.INSERTSPEER
                Logger().resgiterLoggingInfo ("Insert SuperPeers (%s,%s)" % (self.getServerHost(),self.getServerPort()))
            
            resp = self.connectAndSend(host, port, msgHandler, 
                        '%s %s %d' % (self.getPID(),
                                  self.getServerHost(), 
                                  self.getServerPort()))#[0]
           
            
            if (resp[0][0] == AbstractMessageHandler.PEERFULL):
                return False
          
            self.setMySuperPeer("%s:%s"%(host,port))
            
            return True
            
                
        except:
            #traceback.print_exc()
            #print "eerrroooo" 
            self.removePeer(peerID)
    
    def checkLivePeers( self ):
    
        """ Attempts to ping all currently known peers in order to ensure that
        they are still active. Removes any from the peer list that do
        not reply. This function can be used as a simple stabilizer.
    
        """
        todelete = []
        for pid in self.getPeerNeighbors():
            isconnected = False
            try:
                
                host,port,super = self.getPeerNeighbors()[pid]
                peerConn = PeerConnection( pid, host, port)
                peerConn.sendData( 'PING', '' )
                isconnected = True
            except:
                todelete.append( pid )
            if isconnected:
                peerConn.close()
    
        self.getPeerLock().acquire()
        try:
            for pid in todelete: 
                if pid in self.getPeerNeighbors():
                    del self.getPeerNeighbors()[pid]
        finally:
            self.getPeerLock().release()
        

  
    def connected(self): 
        self.__isConnected = True
    
   
    def isConnected(self,peerNeighbor):
        return self.hasNeighbor(peerNeighbor)
       
         
    def setServices(self, serviceRepository):
        self.__services = serviceRepositoy
        return self.__services
    
  
    
    def setConnectionTime(self, time):
        self.__connectionTime = time
    
    
    def getConnectionTime(self):
        return self.__connectionTime
    
               
    def setDisconnectionTime(self, time):
        self.__disconnectionTime = time
    
    
    def getDisconnectionTime(self):
        return self.__disconnectionTime
    
    
    def setScheduledForDisconnection(self, flag):
        self.__scheduledDisconnection = flag
    
    def getScheduledForDisconnection(self):
        return self.__scheduledDisconnection
    
    
    def getServices(self):
        return self.__services
    
    def getDirectTrust(self):
        return self.__directTrust
    
    def getTrustManager(self):
        return self.__trustManager
        
    
    def getSharedResource(self):    
        return self.__sharedResource
    
    
    def getHistoryResource(self):    
        return self.__historyResource
    
    def getEquivalences(self):
        return self.__equivalences
    
    
    def getPeerNeighbors(self):
        return self.__peerNeighbors
    
    def hasPeerNeighbor(self, peerNeighborID):
        return self.__peerNeighbors.has_key(peerNeighborID)
    
   
    def getPeerNeighbor(self, peerID):
        return self.__peerNeighbors[peerID]
    
    
    def addPeerNeighbor( self, peerID, host, port ):
    
        """ Adds a peer name and host:port mapping to the known list of peers.
        
        """
       
        
        if peerID not in self.getPeerNeighbors() and (self.getMaxPeers() == 0 or len(self.getPeerNeighbors()) < self.getMaxPeers()):
            self.getPeerNeighbors()[ peerID ] = (host, int(port))
           
            '''print "Iam =------->",self.getPID()        
            print "Super peer +>",peerID
            print "neighbors",self.getPeerNeighbors().keys() 
           '''
            return True
        else:
            return False

    def getPeer( self, peerID ):
    
        """ Returns the (host, port) tuple for the given peer name """
        assert peerID in self.getPeerNeighbors()    # maybe make this just a return NULL?
        return self.getPeerNeighbors()[ peerID ]
    
    def removePeer( self, peerID ):
    
        """ Removes peer information from the known list of peers. """
        if peerID in self.getPeerNeighbors():
            del self.getPeerNeighbors()[ peerID ]

    
    def addPeerAt( self, loc, peerID, host, port,super ):
    
        """ Inserts a peer's information at a specific position in the 
        list of peers. The functions addpeerat, getpeerat, and removepeerat
        should not be used concurrently with addpeer, getpeer, and/or 
        removepeer. 
    
        """
        self.getPeerNeighbors()[ loc ] = (peerID, host, int(port),super)

   
    def getPeerAt( self, loc ):
    
        if loc not in self.getPeerNeighbors():
            return None
        return self.getPeerNeighbors()[ loc ]

   
    def removePeerAt( self, loc ):
    
           removePeer( self, loc ) 

   
    def getPeerIDs( self ):
    
        """ Return a list of all known peer id's. """
        return self.getPeerNeighbors().keys()


    def numberOfPeers( self ):
   
        """ Return the number of known peer's. """
        return len(self.getPeerNeighbors())
 
    def maxPeersReached( self ):
       
        """ Returns whether the maximum limit of names has been added to the
        list of known peers. Always returns True if maxPeers is set to
        0.
    
        """
        assert self.getMaxPeers() == 0 or len(self.getPeerNeighbors()) <= self.getMaxPeers()
        return self.getMaxPeers() > 0 and len(self.getPeerNeighbors()) == self.getMaxPeers()
    
    def createServices(self,tam=7):
        optionMap   = [ServiceMap(),HardwareMap()]
        optionClass = [Service,Hardware]
       
        
        for i in range(0,randint(1,tam)):
            option = randint(0,1)
            #resourceMap = ResourceMap(optionMap[option])
            resourceMap = ResourceMap(optionMap[1])
         
            map = resourceMap.Map()
            
            concept = map.keys()[randint(0, len(map.keys()) - 1)]
            resour  = randint(0, (len(map[concept]) - 1))
                    
            service = optionClass[option](pid=createURN("peer"),resource=map[concept][resour])
            self.getServices().addElement(service)
        
       
        

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
                
                
                