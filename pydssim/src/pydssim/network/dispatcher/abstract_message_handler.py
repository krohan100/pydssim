from pysocialsim.base.object import Object
from pysocialsim.base.decorator.require import require
from pysocialsim.p2p.peer.i_peer import IPeer
from pysocialsim.base.decorator.public import public
from pysocialsim.base.decorator.return_type import return_type
from pysocialsim.p2p.message.i_p2p_message import IP2PMessage

class AbstractMessageHandler(Object):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, messageName, peer):
        self.__messageName = messageName
        self.__peer = peer
        self.__message = None
    
    @public
    def getMessageName(self):
        return self.__messageName
    
    @public
    def getPeer(self):
        return self.__peer
    
    @public
    def getP2PMessage(self):
        return self.__message
    
    @public
    def handleP2PMessage(self, message):
        self.__message = message
        return self.executeHandler()
        
    def executeHandler(self):
        raise NotImplementedError()