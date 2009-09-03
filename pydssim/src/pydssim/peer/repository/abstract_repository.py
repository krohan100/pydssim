from pydssim.util.protected import Protected
from pydssim.peer.i_peer import IPeer
from pydssim.util.decorator.public import public
from pydssim.util.decorator.public import return_type
from sets import ImmutableSet

class AbstractRepository(Protected):
    
    def __init__(self, peer):
        raise NotImplementedError()
    
    def initialize(self, peer):
        self.__peer = peer
        self.__elements = {}
        
    
    @public
    def addElement(self, element):
        key = element.getUUID()+element.getPID()
        if not self.__elements.has_key(key):
            self.__elements[key] = element
        
        return element
    
    @public
    def removeElement(self, element):
        key = element.getUUID()+element.getPID()
        if not self.__elements.has_key(key):
            raise StandardError()
        if self.__elements[key] > 0:
            del self.__elements[element]
            
        return element
    
    @public
    @return_type(int)
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
    