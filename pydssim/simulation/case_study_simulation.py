'''
Created on 27/10/2009

@author: LGustavo
'''
from pydssim.simulation.reciprocal_trade_simulation_p2p import ReciprocalTradeSimulationP2P
from pydssim.simulation.process.factory.begin_simulation_process_factory import BeginSimulationProcessFactory

simulation = ReciprocalTradeSimulationP2P()
simulation.setSimulationTime(500000)
simulation.initializeNetwork(50, 300, 7)
simulation.addSimulationProcessFactory(BeginSimulationProcessFactory(simulation.getSimulation()))
