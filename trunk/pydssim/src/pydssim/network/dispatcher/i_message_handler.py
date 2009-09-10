from pysocialsim.base.interface import Interface

class IMessageHandler(object):
    
    __metaclass__ = Interface
    
    def __init__(self):
        raise NotImplementedError()
    
    def getMessageName(self):
        raise NotImplementedError()
    
    def getPeer(self):
        raise NotImplementedError()
    
    def getMessage(self):
        raise NotImplementedError()
    
    def clone(self):
        raise NotImplementedError()
    
    def handleMessage(self, message):
        raise NotImplementedError()