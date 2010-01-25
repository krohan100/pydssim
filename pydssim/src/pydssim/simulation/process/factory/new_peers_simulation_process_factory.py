"""
Defines the module with the implementation AbstractSimulationProcessFactory class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""
from __future__ import with_statement
from rpyc import Service, async
from rpyc.utils.server import ThreadedServer
import thread 

from pydssim.simulation.process.factory.abstract_simulation_process_factory import AbstractSimulationProcessFactory
from pydssim.util.decorator.public import public
from pydssim.simulation.process.new_peers_simulation_process import NewPeersSimulationProcess
from pydssim.peer.default_peer import DefaultPeer
from pydssim.peer.rpyc_peer import RPyCPeer
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
        
   
    def factorySimulationProcess(self):
        
        import socket
        ipAddress = socket.gethostbyname(socket.gethostname())
        logMsg =  'Network interface IP address using %s   ...' % ipAddress
        Logger().resgiterLoggingInfo(logMsg)
        
        simulation = self.getSimulation()
        network    = simulation.getNetwork()
        peer_number = 0
        ###
        threads = []
        
        nloops = range(0,7)
        ###
        startPort = 4000
        port = startPort+1
        peer1 = RPyCPeer(network,"peer1",3000)
        network.addPeer(peer1)
        t1 = ThreadedServer(RPyCPeer,ipAddress,3000)
        threads.append(t1)
        ##thread.start_new_thread(t1.start())
        #t.start()
        while ( ( simulation.getSimInstance().now() < simulation.getSimulationTime() ) and ( peer_number < simulation.getNetwork().getPeers())):
            peer_number+=1 
            
            urn = "urn:peer:"+uuid.uuid1().__str__()
            logMsg = "Factoring Process %s => Simulation Time %10.2f making peer number : %s id %s" % (self.getName(),simulation.getSimInstance().now() ,peer_number, urn) 
            Logger().resgiterLoggingInfo(logMsg)
            #print logMsg
            #peer = DefaultPeer(network,urn,port)
            peer = RPyCPeer(network,urn,port)
            peer.createServices(simulation.getResourcePeer())
            network.addPeer(peer)
            t = ThreadedServer(RPyCPeer, ipAddress,port)
            threads.append(t)
            ##thread.start_new_thread(t.start()) # will run on another thread
            #t.start()
            
            peer.createConnection(peer1)
            port += 1
           
            
          
            yield hold, self, simulation.getNetwork().getNewPeerTime()*random() 
        nloops = range(1,peer_number)    
        for i in nloops:            # start threads
            threads[i].start()

        for i in nloops:            # wait for all
            threads[i].join()       #    
        #twisted.internet.reactor.run()
            
       
            
      