"""
Defines the module with the implementation of AbstractSimulationEvent class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 5/07/2009
"""
from pydssim.util.protected import Protected
from pydssim.simulation.process.i_simulation_process import ISimulationProcess
from pydssim.util.decorator.public import public
from SimPy.Simulation import Process

class AbstractSimulationProcess(Process,ISimulationProcess, Protected):
    """
    Abstract class that implemenents the ISimulationEvent interface.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 5/07/2009
    """
      
    def __init__(self):
        raise NotImplementedError()
    
    @public
    def initialize(self, identifier, peer=None, priority=0):
        """
        Initializes the object.
        @param identifier: identifier of simulation event
        @type identifier: str
        @param peerId: peerId of simulation event
        @type peerId: int
        @param priority: priority of simulation event.
        @type priority: int
        @rtype: None
        @note: All simulation events are initialized as unhandled.
        """
        
        Process.__init__(self,name=identifier)
        
        self.__identifier = identifier
        self.__peer = peer
        self.__priority = priority
        self.__isIdentified = False
    
    @public
    def getIdentifier(self):
        return self.__identifier

    @public
    def getPeer(self):
        return self.__peer

    @public
    def getPriority(self):
        return self.__priority
    
    @public
    def identified(self):
        self.__isIdentified = True

    @public
    def isIdentified(self):
        return self.__isIdentified
    
    def execute(self):
        """
        Template method to implement specific algorithm for handling a given simulation event.
        This method must be implemented in AbstractSimulationEventHandler subclasses.
        @note: The visibility of this operation is protected.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    def __eq__(self, other):
        if not other:
            return False
        return self.__identifier == other.getIdentifier() and self.__peerId == other.getPeerId() and self.__priority == other.getPriority()
    
    identifier = property(getIdentifier, None, None, None)
    """
    @type: str 
    """

    peer = property(getPeer, None, None, None)
    """
    @type: IPeer 
    """

    priority = property(getPriority, None, None, None)
    """
    @type: str 
    """
    
    