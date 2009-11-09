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
from multiprocessing import Semaphore
from SimPy.Simulation import Simulation
from pydssim.util.logger import Logger

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
        self.__simInstance = Simulation() 
        
        self.__simulationTime = 0
        self.__currentSimulationTime = 0
        self.__network = None
        self.__simulationProcessFactory = []
        self.__resourcePeer = 0
        Logger().resgiterLoggingInfo("Create Simulation ")

    
    @public
    def initializeNetwork(self, peers ,newPeerTime ,neighbors):
        raise NotImplementedError() 

    @public
    def addSimulationProcessFactory(self, simulationProcessFactory):
       
        if simulationProcessFactory in self.__simulationProcessFactory:
            return None
        self.__simulationProcessFactory.append(simulationProcessFactory)
        simulationProcessFactory.setSimulation(self)
        simulationProcessFactory.initializeProcess()
        
        return self.__simulationProcessFactory[self.__simulationProcessFactory.index(simulationProcessFactory)]

    @public
    def removeSimulationProcessFactory(self, simulationProcessFactory):
       
        if not simulationProcessFactory in self.__simulationProcessFactory:
            return None
        self.__simulationProcessFactory.remove(simulationProcessFactory)
        return simulationProcessFactory

    @public
    def getSimulationProcessFactorys(self):
        return self.__simulationProcessFactory

    @public
    def countSimulationProcessFactorys(self):
        return len(self.__simulationProcessFactory)
    
    @public    
    def configure(self):
        raise NotImplementedError()
    
    @public    
    def getNetwork(self):
        return self.__network
    
    @public
    def setNetwork(self, network):
        
        self.__network = network
        self.__network.setSimulation(self)
        return self.__network
    
    @public    
    def getSimulationTime(self):
        return self.__simulationTime

    @public
    def setSimulationTime(self, simulationTime):
        
        self.__simulationTime = simulationTime
        return self.__simulationTime
    
    @public    
    def getResourcePeer(self):
        return self.__resourcePeer

    @public
    def setResourcePeer(self, resourcePeer):
        
        self.__resourcePeer = resourcePeer
        return self.__resourcePeer
    
    @public
    def getCurrentSimulationTime(self):
        semaphore = Semaphore()
        semaphore.acquire()
        time = self.__currentSimulationTime
        semaphore.release()
        return time
    
    @public
    def setCurrentSimulationTime(self, currentSimulationTime):
       
        semaphore = Semaphore()
        semaphore.acquire()
        self.__currentSimulationTime = currentSimulationTime
        semaphore.release()
        return self.__currentSimulationTime
    
    @public
    def getSimInstance(self):
        return self.__simInstance
    
        
    @public
    def start(self):
        mySim = self.getSimInstance()
        
        factoryProcess = 0
        for factory in self.__simulationProcessFactory:
            print factory.getName()
            mySim.activate( factory, factory.factorySimulationProcess() ) 
            factoryProcess +=1
            
            
        mySim.simulate( until = self.getSimulationTime() )    
        return factoryProcess
       
    
    @public
    def stop(self):
        raise NotImplementedError()
       
    
    
    simInstance = property(getSimInstance, None, None, None)
   
    simulationTime = property(getSimulationTime, setSimulationTime, None, None)
    
    currentSimulationTime = property(getCurrentSimulationTime, setCurrentSimulationTime, None, None)
   
    network = property(getNetwork, setNetwork, None, None)
    
    