from pydssim.util.interface import Interface

class IMessage(object):
    
    __metaclass__ = Interface
    
    def __init__(self):
        raise NotImplementedError()
    
    def getSourceId(self):
        raise NotImplementedError()
    
    def getTargetId(self):
        raise NotImplementedError()
    
    def getTTL(self):
        raise NotImplementedError()
    
    def registerTrace(self, id):
        raise NotImplementedError()
    
    def unregisterTrace(self):
        raise NotImplementedError()
    
    def countTraces(self):
        raise NotImplementedError()
    
    def getTrace(self, index):
        raise NotImplementedError()
    
    def getTraces(self):
        raise NotImplementedError()
    
    def getFirstTrace(self):
        raise NotImplementedError()
    
    def getLastTrace(self):
        raise NotImplementedError()
    
    def getName(self):
        raise NotImplementedError()
    
    def handled(self):
        raise NotImplementedError()
    
    def isHandled(self):
        raise NotImplementedError()
    
    def setHop(self, hop):
        raise NotImplementedError()
    
    def getHop(self):
        raise NotImplementedError()
    
    def setSourceId(self, sourceId):
        raise NotImplementedError()
    
    def setTargetId(self, targetId):
        raise NotImplementedError()
    
    def clone(self):
        raise NotImplementedError()
    
    def setParameter(self, name, value):
        raise NotImplementedError()
    
    def getParameter(self, name):
        raise NotImplementedError()
    
    def removeParameter(self, name):
        raise NotImplementedError()
    
    def getId(self):
        raise NotImplementedError()
    
    def countParameters(self):
        raise NotImplementedError()
    
    def getPriority(self):
        raise NotImplementedError()
    
    def getParameterNames(self):
        raise NotImplementedError()
    
    def getParameterValues(self):
        raise NotImplementedError()