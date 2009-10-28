"""
Defines the module with the implementation of AbstractSimulation class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@vocs.ufrj.br 
@since: 25/10/2009
"""

from pydssim.simulation.abstract_simulation import AbstractSimulation

class ReciprocalTradeSimulationP2P(AbstractSimulation):
    
    def __init__(self):
        AbstractSimulation.initialize(self)