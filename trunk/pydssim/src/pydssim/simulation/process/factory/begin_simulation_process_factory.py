"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory
from pydssim.util.decorator.public import public
from pydssim.simulation.process.begin_simulation_process import BeginSimulationProcess

class BeginSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self,simInstance=None):
        AbstractSimulationProcessFactory.initialize(self,"Begin Simulation Process Factory",simInstance)
        
    
    @public
    def factorySimulationProcess(self):
        simulation = self.getSimulation()
        event = BeginSimulationProcess()
        simulation.registerSimulationEvent(event)
        return 1