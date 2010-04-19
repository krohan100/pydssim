"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

import threading
from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory

from pydssim.peer.super_peer import SuperPeer

from pydssim.peer.abstract_peer import AbstractPeer

from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *
from random import random
import uuid

class NewSuperPeersSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW SUPERPEER PROCESS FACTORY")
        
   
    def factorySimulationProcess(self):
        
               
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
       
        ###
        port = 3001
      
        portalID = network.getPortalID()
        totalSP = simulation.getNetwork().getPeers()/simulation.getNetwork().getMaxNeighbor()
        
        while ( ( simulation.getSimInstance().now() < simulation.getSimulationTime() ) and ( peer_number < totalSP )):
            peer_number+=1 
            
            urn = "urn:superpeer:"+uuid.uuid1().__str__()
            logMsg = "Factoring Process %s => Simulation Time %10.2f making peer number : %s id %s" % (self.getName(),simulation.getSimInstance().now() ,peer_number, urn) 
            SimulationProcessLogger().resgiterLoggingInfo(logMsg)
            
            peer = SuperPeer(urn,port,simulation.getNetwork().getMaxNeighbor())
           
           
            network.addPeer(peer)
            #peer.newSuperPeer(portalID)
            peer.connectPortal(portalID,1)
            
            t = threading.Thread( target = peer.mainLoop,
                              args = [] )
            t.start()
                      
            port += 1
           
            yield hold, self, simulation.getNetwork().getNewPeerTime()*random()*(peer_number)#*2)
            
        
       
            
      