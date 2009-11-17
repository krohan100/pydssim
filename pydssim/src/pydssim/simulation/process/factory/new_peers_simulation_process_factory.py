"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory
from pydssim.util.decorator.public import public
from pydssim.simulation.process.new_peers_simulation_process import NewPeersSimulationProcess
from pydssim.peer.default_peer import DefaultPeer
from pydssim.util.logger import Logger
from SimPy.Simulation import *
from random import random
import uuid

class NewPeersSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW PEER PROCESS FACTORY")
        
    
    @public
    def factorySimulationProcess(self):
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
        
        while ( ( simulation.getSimInstance().now() < simulation.getSimulationTime() ) and ( peer_number < simulation.getNetwork().getPeers())):
            peer_number+=1 
            
            pid = "urn:peer:id:"+uuid.uuid1().__str__()
            logMsg = "Factoring Process %s => Simulation Time %10.2f making peer number : %s id %s" % (self.getName(),simulation.getSimInstance().now() ,peer_number, pid) 
            Logger().resgiterLoggingInfo(logMsg)
            #print logMsg
            peer = DefaultPeer(network,pid)
            peer.createServices(simulation.getResourcePeer())
            network.addPeer(peer)
            
          
            yield hold, self, simulation.getNetwork().getNewPeerTime()*random() 
            
       
            
      