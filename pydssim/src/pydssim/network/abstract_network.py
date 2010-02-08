
from sets import ImmutableSet
from multiprocessing import Semaphore
from pydssim.peer.neighbor.neighbor import Neighbor
from pydssim.util.logger import Logger




class AbstractNetwork():
    """
    Defines the operations of Network .

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """
 
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, simulation, peers , newPeerTime, maxNeighbors,portal,startPort=3999):
        
        self.__simulation = simulation
        self.__portalID = portal+":%s"%startPort
        
        self.__startPort = startPort
        
        self.__connectedPeers = {}
        self.__advertisedPeers = []
        self.__layout = {} 
        self.__peers = peers
        self.__newPeerTime = newPeerTime
        self.__maxNeighbors = maxNeighbors
        Logger().resgiterLoggingInfo("Initialize Network => peers = %d , New Peer Time = %d, neighbors/peer = %d "%(peers,newPeerTime,maxNeighbors))
    
    
    def getSimulation(self):
        return self.__simulation
    
    def getPortalID(self):
        return self.__portalID
    
    def setSimulation(self, simulation):
        self.__simulation = simulation
        return self.__simulation
    
    
    def getPeers(self):
        return self.__peers
    
    
    def getNewPeerTime(self):
        return self.__newPeerTime
    
    
    def getLayout(self):
        return self.__layout
    
    
    def setLayout(self, layout):
        self.__layout = layout
        return self.__layout
    
    
    def countPeers(self):
        semaphore = Semaphore()
        semaphore.acquire()
        tamPeers = len(self.__layout)
        semaphore.release()
        return tamPeers
   
    
    def addPeer(self, peer):
        
        if self.__layout.has_key(peer.getPID()):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        
        self.__layout[peer.getPID()] = peer
        semaphore.release()
        Logger().resgiterLoggingInfo("Add peer %s in Layout Network "%(peer.getPID()))
        return self.__layout.has_key(peer.getPID())

    
    def removePeer(self, peer):
        
        flag = True
        
        if not self.__layout.has_key(peer.getPID()):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        
        '''
        pode travar  pois estou chamando um sema dentro do outro?
        '''
        neighbors = peer.getPID().getNeighbors()  
        
        if  len(neighbors) != 0:
            for target in  neighbors:
                self.removeNeighbor(peer.getPID(), target) 
        
        del self.__layout[peer.getPID().getId()]
        del self.__connectedPeers[peer.getPID()]
        
        flag = not self.__layout.has_key(peer.getPID())
        semaphore.release()
        
        return flag

   
    def getMaxNeighbor(self):
        return self.__maxNeighbors
         
    
    def getPeer(self, peerId):
        
        semaphore = Semaphore()
        semaphore.acquire()
        peer = self.__layout[peerId]
        semaphore.release()
        return peer
    
    
    def getNeighbors(self, peer):
        
        if not self.__layout.has_key(peer.getPID()):
            return ImmutableSet([])
        return layout[peer.getPID()].getNeighbors()
    
     
    
    def dispatchMessage(self, message):
        sem = Semaphore()
        sem.acquire()
        peer = self.getPeer(message.getTargetId())
        peer.receive(message)
        sem.release()
        return message
    
    
    def isNeighbor(self, source, target):
        sem = Semaphore()
        sem.acquire()
        
        aux = source.hasNeighbor(target)
        
        sem.release()
        return aux
    
    
    def createConnection(self, source, target):
       
        if source == target:
            raise StandardError()
        
       
        #if (not self.__layout.has_key(source.getPID()) or (not self.__layout.has_key(target.getPID()))):
        #    raise StandardError()
        if (source.hasNeighbor( target)):
            return True
        
      
        
        sem = Semaphore()
        sem.acquire()
       
        self.getPeer(source.getPID()).addNeighbor(Neighbor(target))
        self.getPeer(target.getPID()).addNeighbor(Neighbor(source))
       
        
        self.__connectedPeers[target.getPID()] = target
        self.__connectedPeers[source.getPID()] = source
        
        sem.release()
        return self.isNeighbor(source, target)
    
    
    def removeConnection(self, source, target):
        
        if isinstance(source.getPID(), bool) or isinstance(target.getPID(), bool):
            raise TypeError()
        if source == target:
            raise StandardError()
        if (not self.__layout.has_key(source.getPID())) or (not self.__layout.has_key(target.getPID())):
            raise StandardError()
        if (self.isNeighbor(source, target) == False):
            return False
        
        sem = Semaphore()
        sem.acquire()
        
        source.removeConnection(target)
        targer.removeConnection(source)
        
               
        if len(self.getNeighbors(source)) ==0 :
             del self.__connectedPeers[source.getId()]
        
        if len(self.getNeighbors(target)) ==0 :
             del self.__connectedPeers[target.getId()]
        
        self.__connectedPeers.remove(soruce)
        
        sem.release()
        
        return not self.isNeighbor(source, target)
    
   
    
    def getPeerForConnection(self):
         
        if (len(self.__layout) == 0) or (len(self.__layout) == len(self.__connectedPeers)):
            return None
                        
        while True:
            peerKey = self.__layout.keys()[randint(0, len(self.__layout.keys()) - 1)]
            if not self.__connectedPeers.has_key(peerKey):
                return self.__layout[peerKey]
        
    
    
    def getPeerForDisconnection(self):
        if len(self.__connectedPeers) == 0:
            return None
        
        peerKey = self.__connectedPeers.keys()[randint(0, len(self.__connectedPeers.keys()) - 1)]
        
        return self.__connectedPeers[peerKey]
    
   
    def countConnectedPeers(self):
        return len(self.__connectedPeers)
    
    
    def countDisconnectedPeers(self):
        return len(self.__layout) - self.countConnectedPeers()
    
   
    def getConnectedPeers(self):
        return self.__connectedPeers
    

    