"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.util.protected import Protected
from pydssim.simulation.process.factory.i_simualtor_process_factory import ISimulationProcessFactory
from SimPy.Simulation import Process
from pydssim.util.logger import Logger

class AbstractSimulationProcessFactory( ISimulationProcessFactory,Process):
    """
    Defines the basic implementation of ISimulationProcessFactory interface.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self,name):
        self.__name = name
        self.__simulation = None
        
        Logger().resgiterLoggingInfo("Initialize "+name)
    
    
    def initializeProcess(self):
                
        return Process.__init__( self, self.getName(), self.getSimulation().getSimInstance())
        
        
        
    def getSimulation(self):
        return self.__simulation

    
    def setSimulation(self, simulation):
        
        self.__simulation = simulation
        return self.__simulation
    
        
    def getName(self):
        return self.__name

   
    def factorySimulationProcess(self):
        return ISimulationProcessFactory.factorySimulationProcess(self)
    
    
    
