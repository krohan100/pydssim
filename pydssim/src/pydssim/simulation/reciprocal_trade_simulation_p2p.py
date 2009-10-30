"""
Defines the module with the implementation of AbstractSimulation class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@vocs.ufrj.br 
@since: 25/10/2009
"""

from pydssim.simulation.abstract_simulation import AbstractSimulation
from pydssim.network.p2p_network import P2PNetwork
from pydssim.util.decorator.public import public

class ReciprocalTradeSimulationP2P(AbstractSimulation):
    
    def __init__(self):
        AbstractSimulation.initialize(self)
        
    @public
    def initializeNetwork(self, peers ,newPeerTime ,neighbors):
        self.__network = P2PNetwork(self, peers, newPeerTime,neighbors)