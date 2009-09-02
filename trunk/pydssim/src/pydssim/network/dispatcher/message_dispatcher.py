from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from threading import Thread

class MessageDispatcher(Protected):
    
    def __init__(self, peer):
        self.initialize(peer)
    
    def initialize(self, peer):
        self.__peer = peer
        self.__messageHandlers = {}
    
    @public
    def registerMessageHandler(self, messageHandler):
        if self.__messageHandlers.has_key(messageHandler.getMessageName()):
            raise StandardError()
        self.__messageHandlers[messageHandler.getMessageName()] = messageHandler
        return self.__messageHandlers[messageHandler.getMessageName()]
    
    @public
    def countMessageHandlers(self):
        return len(self.__messageHandlers)
    
    @public
    def unregisterMessageHandler(self, messageName):
        if not self.__messageHandlers.has_key(messageName):
            raise StandardError()
        messageHandler = self.__messageHandlers[messageName]
        del self.__messageHandlers[messageName]
        return messageHandler
    
    @public
    def handleP2PMessage(self, message):
        if not self.__messageHandlers.has_key(message.getName()):
            raise StandardError()
        handler = self.__messageHandlers[message.getName()]
        handler.handleP2PMessage(message)
#       
        return message
    
    class MessageHandlingThread(Thread):
        
        def __init__(self, handler, message):
            Thread.__init__(self)
            self.__handler = handler
            self.__message = message
            
        def run(self):
            self.__handler.handleP2PMessage(self.__message)