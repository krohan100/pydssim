from pydssim.util.interface import Interface

class INeighbor:
    
    __metaclass__ = Interface
    
    def getId(self):
        raise NotImplementedError()
    
    def addRoute(self, route):
        raise NotImplementedError()
    
    def getPeer(self):
        raise NotImplementedError()