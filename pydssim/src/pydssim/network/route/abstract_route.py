from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public

class AbstractRoute(Object):
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self, type, elementId, trace):
        self.__type = type
        self.__elementId = elementId
        self.__trace = trace
    
    @public
    def getType(self):
        return self.__type
    
    @public
    def getElementId(self):
        return self.__elementId
    
    @public
    def getTrace(self):
        return self.__trace
    
    def __eq__(self, other):
        aux = (self.__type == other.getType()) and (self.__elementId == other.getElementId())
        bln = True
        for t in self.__trace:
            if not t in other.getTrace():
                return False
        return aux and bln