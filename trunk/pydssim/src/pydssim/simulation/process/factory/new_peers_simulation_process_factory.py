"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

import threading
from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory

from pydssim.peer.default_peer import DefaultPeer
from pydssim.peer.portal_peer import PortalPeer
from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.peer.trust.direct_trust import DirectTrust
from pydssim.peer.trust.abstract_trust import AbstractTrust

from pydssim.util.logger import Logger
from SimPy.Simulation import *
from random import random,randint,shuffle

from pydssim.util.data_util import randomDate,strTime
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
        AbstractSimulationProcessFactory.initialize(self,"NEW SIMPLEPEER PROCESS FACTORY")
        
    
    def createTrust(self,peer,peers,transactionNumber,dateTimeStart,dateTimeStop):
       
        keys= peers.keys()
        shuffle(keys)
           
        #directTrust = peer.getDirectTrust()
        directTrust = peer.getTrustManager().getDirectTrust()
        status = [True,False]
        for i in keys: 
        
            peerID,peerN = i, peers[i]
                             
            services = peerN.getServices()
           
            for countEle in range(0,randint(0,services.countElements())):
                
                element = services.getRandonElement()
                #print element.getUUID(),element.getResource()
                
                for countTrans in range(0,randint(0,transactionNumber)):
                    rating= random()
                    
                    
                    period = randomDate(dateTimeStart,dateTimeStop, random())
                    #print "--------------------->>>>>>>>>>>>>>",period, period < randomDate(dateTimeStart,dateTimeStop, random()) 
                    option = randint(0,1)
                    
                    directTrust.addElement(DirectTrust(peerID,element.getUUID(),element.getResource(),AbstractTrust.DIRECT,rating,period,status[option]))
         
               
    def factorySimulationProcess(self):
        
        
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
       
        port = 4000
      
        portalID = network.getPortalID()
      
        while ( ( simulation.getSimInstance().now() < simulation.getSimulationTime() ) and ( peer_number < simulation.getNetwork().getPeers())):
            peer_number+=1 
            
            urn = "urn:peer:"+uuid.uuid1().__str__()
            logMsg = "Factoring Process %s => Simulation Time %10.2f making peer number : %s id %s" % (self.getName(),simulation.getSimInstance().now() ,peer_number, urn) 
            Logger().resgiterLoggingInfo(logMsg)
            
            peer = DefaultPeer(urn,port)
           
            peer.createServices(simulation.getResourcePeer())
            
            network.addPeer(peer)
            peer.connectPortal(portalID)
            
            t = threading.Thread( target = peer.mainLoop,
                              args = [] )
            t.start()
                      
            port += 1
           
            self.createTrust(peer,network.getPeersFromLayout(peer),simulation.getTransactionNumber(),simulation.getTransactionDateTimeStart(),simulation.getTransactionDateTimeStop())
            #print peer.getDirectTrust().countElements()
            
            peerT = network.getRandonPeer()
            
            print "direct ===>>",peer.getTrustManager().directTrustCalculation(peerT.getPID(),"memory",strTime("1/1/2009 1:30 PM"),strTime("12/31/2009 4:50 AM"))
              
            yield hold, self, simulation.getNetwork().getNewPeerTime()*random()
       