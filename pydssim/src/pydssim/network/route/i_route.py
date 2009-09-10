from pydssim.util.interface import Interface

class IRoute:
    
    __metaclass__ = Interface
    
    def getType(self):
        raise NotImplementedError()
    
    def getElementId(self):
        raise NotImplementedError()
    
    def getTrace(self):
        raise NotImplementedError()