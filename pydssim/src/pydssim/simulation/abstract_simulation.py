"""
Defines the module with the implementation of AbstractSimulation class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@vocs.ufrj.br 
@since: 5/07/2009
"""

from pydssim.util.protected import Protected
from pydssim.simulation.i_simulation import ISimulation
from pydssim.util.decorator.public import public
from pysocialsim.common.simulator.event.i_simulation_event import ISimulationEvent
from pysocialsim.common.error.register_simulation_event_error import RegisterSimulationEventError
from pysocialsim.common.error.unregister_simulation_event_error import UnregisterSimulationEventError
from pysocialsim.common.p2p.network.i_peer_to_peer_network import IPeerToPeerNetwork
from pysocialsim.common.simulator.event.i_simulation_event_generator import ISimulationEventGenerator
import time

class AbstractSimulation(Protected, ISimulation):
    """
    Defines the interface of simulation objects.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
   
    """
    
    def __init__(self):
        raise NotImplementedError()

    def initialize(self):
        """
        Initializes the object.
        @rtype: NoneType
        """
        
        self.__simulationTime = 0
        self.__currentSimulationTime = 0
        self.__network = None
        self.__simulationEventGenerators = []
   
    @public
    def addSimulationEventGenerator(self, simulationEventGenerator):
       
        if simulationEventGenerator in self.__simulationEventGenerators:
            return None
        self.__simulationEventGenerators.append(simulationEventGenerator)
        simulationEventGenerator.setSimulation(self)
        return self.__simulationEventGenerators[self.__simulationEventGenerators.index(simulationEventGenerator)]

    @public
    def removeSimulationEventGenerator(self, simulationEventGenerator):
       
        if not simulationEventGenerator in self.__simulationEventGenerators:
            return None
        self.__simulationEventGenerators.remove(simulationEventGenerator)
        return simulationEventGenerator

    @public
    def getSimulationEventGenerators(self):
        return self.__simulationEventGenerators

    @public
    def countSimulationEventGenerators(self):
        return len(self.__simulationEventGenerators)
    
    @public    
    def configure(self):
        handlers = self.__simulator.getSimulationEventHandlers()
        for hndlr in handlers:
            self.__queues[hndlr.getHandle()] = PriorityQueue()
        generatedEvents = 0
        for generator in self.__simulationEventGenerators:
            generatedEvents += generator.generateSimulationEvents()
        return generatedEvents
    
    @public    
    def getPeerToPeerNetwork(self):
        return returns(self.__network, IPeerToPeerNetwork)
    
    @public
    def getSimulationEvent(self, handle):
        requires(handle, str)
        
        pre_condition(handle, lambda x: x <> "")
        pre_condition(handle, lambda x: x <> None)
        pre_condition(handle, lambda x: self.__queues.has_key(x))
        
        return returns(self.__queues[handle].getFirst(), ISimulationEvent)

    @public
    def setPeerToPeerNetwork(self, peerToPeerNetwork):
        requires(peerToPeerNetwork, IPeerToPeerNetwork)
        pre_condition(peerToPeerNetwork, lambda x: x <> None)
        self.__network = peerToPeerNetwork
        self.__network.setSimulation(self)
        return returns(self.__network, IPeerToPeerNetwork)
    
    @public    
    def getSimulationTime(self):
        return returns(self.__simulationTime, int)

    @public
    def setSimulationTime(self, simulationTime):
        requires(simulationTime, int)
        pre_condition(simulationTime, lambda x: x > 0)
        self.__simulationTime = simulationTime
        return returns(self.__simulationTime, int)
    
    @public
    def getCurrentSimulationTime(self):
        semaphore = Semaphore()
        semaphore.acquire()
        time = self.__currentSimulationTime
        semaphore.release()
        return returns(time, int)

    @public
    def setCurrentSimulationTime(self, currentSimulationTime):
        requires(currentSimulationTime, int)
        pre_condition(currentSimulationTime, lambda x: x > 0)
        semaphore = Semaphore()
        semaphore.acquire()
        self.__currentSimulationTime = currentSimulationTime
        semaphore.release()
        return returns(currentSimulationTime, int)
    
    @public
    def getSimulator(self):
        return returns(self.__simulator, ISimulator)
    
    @public
    def setSimulator(self, simulator):
        requires(simulator, ISimulator)
        pre_condition(simulator, lambda x: x <> None)
        self.__simulator = simulator
        return returns(self.__simulator, ISimulator)
    
    @public
    def execute(self):
        self.SimulationEngine(self).start()
    
    @public
    def stop(self):
        for queue in self.__queues.values():
            queue.clear()
    
    @public
    def countSimulationEventQueues(self):
        return len(self.__queues)

    @public
    def countSimulationEvents(self, handle):
        requires(handle, str)
        pre_condition(handle, lambda x: x <> "" or x <> None)
        return returns(self.__queues[handle].size(), int)

    @public
    def registerSimulationEvent(self, simulationEvent):
        requires(simulationEvent, ISimulationEvent)
        pre_condition(simulationEvent, lambda x: x <> None)
        if not self.__queues.has_key(simulationEvent.getHandle()):
            raise RegisterSimulationEventError(simulationEvent.getHandle()+" is invalid handle")
        return returns(self.__queues[simulationEvent.getHandle()].enqueue(simulationEvent, simulationEvent.getPriority()), ISimulationEvent)

    @public
    def unregisterSimulationEvent(self, handle):
        requires(handle, str)
        pre_condition(handle, lambda x: x <> None)
        pre_condition(handle, lambda x: x <> "")
        if not self.__queues.has_key(handle):
            raise UnregisterSimulationEventError(handle + "was not registered by simulator.")
        return returns(self.__queues[handle].dequeue(), ISimulationEvent)
    
    simulator = property(getSimulator, setSimulator, None, None)
    """
    @type: ISimulator 
    """
    simulationTime = property(getSimulationTime, setSimulationTime, None, None)
    """
    @type: int 
    """
    currentSimulationTime = property(getCurrentSimulationTime, setCurrentSimulationTime, None, None)
    """
    @type: int
    """
    peerToPeerNetwork = property(getPeerToPeerNetwork, setPeerToPeerNetwork, None, None)
    """
    @type: IPeerToPeerNetwork 
    """
    