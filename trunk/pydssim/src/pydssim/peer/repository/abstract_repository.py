from pydssim.util.protected import Protected
from pydssim.peer.i_peer import IPeer
from pydssim.util.decorator.public import public
from pydssim.util.decorator.return_type import return_type
from sets import ImmutableSet
from pydssim.util.logger import Logger

class AbstractRepository(Protected):
    
    def __init__(self, peer):
        raise NotImplementedError()
    
    def initialize(self, peer):
        self.__peer = peer
        self.__elements = {}
        Logger().resgiterLoggingInfo("Initialize Repository URN  %s of peer %s "%(self.__class__.__name__,self.__peer.getURN()))
        
    
    @public
    def addElement(self, element):
        key = element.getUUID()
        if not self.__elements.has_key(key):
            self.__elements[key] = element
        
        Logger().resgiterLoggingInfo("Add Service %s - %s in Repository URN  %s of peer %s "%(element.getUUID(),element.getResource(),self.__class__.__name__,self.__peer.getURN()))
        return element
    
    @public
    def removeElement(self, element):
        key = element.getUUID()#+self.__peer.getURN()
        if not self.__elements.has_key(key):
            raise StandardError()
        if self.__elements[key] > 0:
            del self.__elements[element]
            
        return element
    
    @public
    def countElements(self):
        return len(self.__elements)
    
    @public
    @return_type(dict)
    def getElements(self):
        return self.__elements
    
    @public
    @return_type(IPeer)
    def getPeer(self):
        return self.__peer
    