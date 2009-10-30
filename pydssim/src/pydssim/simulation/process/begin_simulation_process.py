
"""
@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 6/07/2009
"""
from pydssim.simulation.process.abstract_simulation_process import AbstractSimulationProcess

class BeginSimulationProcess(AbstractSimulationProcess):
    """
    Defines the implementation of BeginSimulationProcess
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 6/07/2009
    """

    def __init__(self,simInstance=None):
        AbstractSimulationProcess.initialize(self, "BEGIN_SIMULATION",simInstance)
    
    def execute(self):
        return AbstractSimulationProcess.execute(self)
    
    
        