from pydssim.util.protected import Protected
from pydssim.util.decorator.require import require
from pydssim.util.decorator.public import public
from pydssim.util.decorator.return_type import return_type
from pydssim.peer.i_peer import IPeer
from pydssim.network.topology.topology import Topology
from sets import ImmutableSet
from multiprocessing import Semaphore
from pydssim.peer.neighbor import Neighbor
import bisect

class AbstractNetwork(Protected):
    """
    Defines the operations of Network .

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self):
       
        self.__simulation = None
        
        self.__connectedPeers = []
        self.__advertisedPeers = []
        self.__layout = {} 
    
    @public
    def getSimulation(self):
        return self.__simulation
    
    @public
    def setSimulation(self, simulation):
        self.__simulation = simulation
        return self.__simulation
    
    @public
    def countPeers(self):
        semaphore = Semaphore()
        semaphore.acquire()
        tamPeers = len(self.__layout)
        semaphore.release()
        return tamPeers
   
    @public
    def addPeer(self, peer):
        
        if self.__layout.has_key(peer.getId()):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        
        self.__layout[peer.getId()] = peer
        semaphore.release()
        return self.__layout.has_key(peer.getId())

    @public
    def removePeer(self, peer):
        
        flag = True
        
        if not self.__layout.has_key(peer.getId()):
            return False
        
        semaphore = Semaphore()
        semaphore.acquire()
        
        '''
        pode travar  pois estou chamando um sema dentro do outro?
        '''
        neighbors = peer.getNeighbors()  
        
        if  len(neighbors) != 0:
            for target in  neighbors:
                self.removeNeighbor(peer, target) 
        
        del self.__layout[peer.getId()]
        flag = not self.__layout.has_key(peer.getId())
        semaphore.release()
        
        return flag

    @public
    def getPeer(self, peerId):
        
        semaphore = Semaphore()
        semaphore.acquire()
        peer = self.__layout[peerId]
        semaphore.release()
        return peer
    
    @public
    def getNeighbors(self, peer):
        layout = self.__layout
        if not layout.has_key(peer.getPID()):
            return ImmutableSet([])
        return ImmutableSet(layout[peer.getPID()])
    
     
    @public
    def dispatchMessage(self, message):
        sem = Semaphore()
        sem.acquire()
        peer = self.getPeer(message.getTargetId())
        peer.receive(message)
        sem.release()
        return message
    
    @public
    def isNeighbor(self, source, target):
        sem = Semaphore()
        sem.acquire()
        
        aux = source.hasNeighbor(target)
        
        sem.release()
        return aux
    
    @public
    def createConnection(self, source, target):
       
        if source == target:
            raise StandardError()
        layout = self.__layout
        if (not layout.has_key(source.getPID()) or (not layout.has_key(target.getPID()))):
            raise StandardError()
        if (source.hasNeighbor( target)):
            return True
        
        sem = Semaphore()
        sem.acquire()
       
        self.getPeer(source.getPID()).addNeighbor(Neighbor(target))
        self.getPeer(target.getPID()).addNeighbor(Neighbor(source))
        
        self.__connectedPeers.append(target)
        self.__connectedPeers.append(source)
        
        sem.release()
        return self.isNeighbor(source, target)
    
    @public
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
        
        self.__connectedPeers.remove(target)
        self.__connectedPeers.remove(soruce)
        
        sem.release()
        
        return not self.isNeighbor(source, target)
    
   pensar na validade de coloca isso    
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
    def registerPeerForAdvertisement(self, peer):
        self.__advertisedPeers.append(peer)
        return self.__advertisedPeers[self.__advertisedPeers.index(peer)]
    
    @public
    def getPeerForAdvertisement(self):
        return self.__advertisedPeers[0]
    
    @public
    def unregisterPeerForAdvertisement(self, peer):
        return self.__advertisedPeers.pop(self.__advertisedPeers.index(peer))
    
    @public
    def getConnectedPeers(self):
        return self.__connectedPeers