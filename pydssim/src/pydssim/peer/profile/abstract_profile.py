from pydssim.util.protected import Protected
from pydssim.peer.i_peer import IPeer
from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.util.decorator.public import public
from pydssim.util.decorator.public import return_type
from sets import ImmutableSet

class AbstractProfile(Protected):
    
    def __init__(self, peer):
        raise NotImplementedError()
    
    def initialize(self, peer):
        self.__peer = peer
        self.__resources = {}
        self.__equivalence = {0: []}
        self.__nameUser = ''
        
    
    @public
    def addResource(self, resource):
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
    @return_type(IPeer)
    def getPeer(self):
        return self.__peer
    