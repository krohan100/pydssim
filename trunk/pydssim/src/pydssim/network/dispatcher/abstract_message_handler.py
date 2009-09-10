from pydssim.util.protected import Protected
from pydssim.util.decorator.require import require
from pydssim.util.decorator.public import public
from pydssim.util.decorator.return_type import return_type
from pydssim.network.message.i_message import IMessage

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
    def getMessage(self):
        return self.__message
    
    @public
    def handleMessage(self, message):
        self.__message = message
        return self.executeHandler()
        
    def executeHandler(self):
        raise NotImplementedError()