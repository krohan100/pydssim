"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

import threading
from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory


from pydssim.util.log.simulation_process_logger import SimulationProcessLogger
from SimPy.Simulation import *
from random import random,randint,shuffle
from pydssim.peer.trading.abstract_trading import AbstractTrading
from pydssim.util.data_util import randomDate,strTime
import uuid

class NewTradingSimulationProcessFactory(AbstractSimulationProcessFactory):
    """
    Defines the the implementation of BeginSimulationProcessFactory.
    @author: Luiz Gustavo 
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 28/10/2009
    """

    def __init__(self):
        AbstractSimulationProcessFactory.initialize(self,"NEW TRADING PROCESS FACTORY")
        
    
   
                               
    def factorySimulationProcess(self):
        
        
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        
      
        while  (simulation.getSimInstance().now() < simulation.getSimulationTime()):
             
            yield hold, self, simulation.getNetwork().getNewPeerTime()*random()*10
            peer = network.getRandonPeer()
            services = peer.getServices()
            
            if services.countElements()>=2:
                urn = "urn:trading:"+uuid.uuid1().__str__()
                logMsg = "Factoring Process %s => Simulation Time %10.2f making  : id %s" % (self.getName(),simulation.getSimInstance().now() , urn) 
                SimulationProcessLogger().resgiterLoggingInfo(logMsg)
                
                periodStart = randomDate(simulation.getTransactionDateTimeStart(),simulation.getTransactionDateTimeStop(), random())
                periodEnd = randomDate(periodStart,simulation.getTransactionDateTimeStop(), random()) 
                serviceQuantity = 5#randint(1,10)
            
            
                service = services.getElements().values()[randint(0,services.countElements()-1)]
                print " NEEWWW ",service.getResource()
             
                peer.getTradingManager().creatTradingService(service,periodStart,periodEnd,serviceQuantity,AbstractTrading.CLIENT)
            
              
              
            
       