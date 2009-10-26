"""
Defines the module with the specification of ISimulation interface.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@vocs.ufrj.br 
@since: 5/07/2009
"""

class ISimulation(object):
    """
    Defines the interface of simulation objects.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
   
    """
    
    def __init__(self):
        raise NotImplementedError()
    
    def execute(self):
        """
        Executes the simulation.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    def configure(self):
        """
        Configures the simulation.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    def stop(self):
        """
        Stops the simulation.
        @rtype: NoneType
        """
        raise NotImplementedError()
    
    def getSimulationTime(self):
        """
        Gets the during time of simulation.
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def setSimulationTime(self, simulationTime):
        """
        Sets a time of simulation.
        @param simulationTime: an int
        @type simulationTime: int
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def setPeerToPeerNetwork(self, peerToPeerNetwork):
        """
        Sets a peer-to-peer network object.
        @param peerToPeerNetwork: an IPeerToPeerNetwork
        @type peerToPeerNetwork: IPeerToPeerNetwork
        @return: an IPeerToPeerNetwork
        @rtype: IPeerToPeerNetwork
        """
        raise NotImplementedError()
    
    def getPeerToPeerNetwork(self):
        """
        Gets a peer-to-peer network object.
        @return: an IPeerToPeerNetwork
        @rtype: IPeerToPeerNetwork
        """
        raise NotImplementedError()
    
    def getCurrentSimulationTime(self):
        """
        Gets the current time of simulation.
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def countSimulationEvents(self, handle):
        """
        Counts simulation events registered by simulation object.
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def getSimulationEvent(self, handle):
        """
        Gets the first simulation event in priority queue.
        @return: a ISimulationEvent
        @rtype: ISimulationEvent
        """
        raise NotImplementedError()
    
    def registerSimulationEvent(self, simulationEvent):
        """
        Registries a simulation event in simulation.
        @param simulationEvent: an ISimulationEvent
        @type simulationEvent: ISimulationEvent
        @return: an ISimulationEvent
        @rtype: ISimulationEvent
        """
        raise NotImplementedError()
    
    def unregisterSimulationEvent(self, handle):
        """
        Unregistries a simulation event in queue of events.
        @param handle: a str
        @type handle: str
        @return: an ISimulationEvent
        @rtype: ISimulationEvent
        """
        raise NotImplementedError()
    
    def setCurrentSimulationTime(self, currentSimulationTime):
        """
        Sets the current time of simulation.
        @param currentSimulationTime: an int
        @type currentSimulationTime: int
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def setSimulator(self, simulator):
        """
        Sets a simulator.
        @param simulator: an ISimulator
        @type simulator: ISimulator
        @return: an ISimulator
        @rtype: ISimulator
        """
        raise NotImplementedError()
    
    def getSimulator(self):
        """
        Sets a simulator.
        @return: an ISimulator
        @rtype: ISimulator
        """
        raise NotImplementedError()
    
    def countSimulationEventQueues(self):
        """
        Counts queues of simulation events.
        @return: a int
        @rtype: int
        """
        raise NotImplementedError()
    
    def addSimulationEventGenerator(self, simulationEventGenerator):
        """
        Adds a simulation event generator.
        @param simulationEventGenerator: an ISimulationEventGenerator
        @return: a ISimulationEventGenerator
        @rtype: ISimulationEventGenerator
        """
        raise NotImplementedError()
    
    def removeSimulationEventGenerator(self, simulationEventGenerator):
        """
        Removes a simulation event generator.
        @param simulationEventGenerator: an ISimulationEventGenerator
        @return: a ISimulationEventGenerator
        @rtype: ISimulationEventGenerator
        """
        raise NotImplementedError()
    
    def getSimulationEventGenerators(self):
        """
        Gets a list of simulation event generators.
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def countSimulationEventGenerators(self):
        """
        Counts simulation event generators.
        @return: a int
        @rtype: int
        """
        raise NotImplementedError()
    
