'''
Created on 24/04/2010

@author: Luiz Gustavo
'''

from pydssim.peer.history.abstract_history import AbstractHistory

class History(AbstractHistory):
    '''
    classdocs
    '''

    def __init__(self, peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingQuantity,equivalenceEquivalenceResource,
        equivalenceEquivalenceUUID,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd):
        '''
        Constructor
        '''
        self.initialize( peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingQuantity,equivalenceEquivalenceResource,
        equivalenceEquivalenceUUID,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd)
        
    def initialize(self,  peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingQuantity,equivalenceEquivalenceResource,
        equivalenceEquivalenceUUID,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd):
        
        AbstractTrading.initialize(self,  peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingQuantity,equivalenceEquivalenceResource,
        equivalenceEquivalenceUUID,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd)