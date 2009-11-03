'''
Created on 27/10/2009

@author: LGustavo
'''
from pydssim.simulation.reciprocal_trade_simulation_p2p import ReciprocalTradeSimulationP2P
from pydssim.simulation.process.factory.begin_simulation_process_factory import BeginSimulationProcessFactory
from pydssim.simulation.process.factory.new_peers_simulation_process_factory import NewPeersSimulationProcessFactory

simulation = ReciprocalTradeSimulationP2P()
simulation.setSimulationTime(500000000000000)
simulation.initializeNetwork(50, 300000, 7)
simulation.addSimulationProcessFactory(NewPeersSimulationProcessFactory())
simulation.addSimulationProcessFactory(BeginSimulationProcessFactory())
print simulation.start()
