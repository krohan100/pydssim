'''
Created on 24/04/2010

@author: Luiz Gustavo
'''

from pydssim.peer.trading.abstract_trading import AbstractTrading

class TradingService(AbstractTrading):
    '''
    classdocs
    '''

    def __init__(self,service,periodStart,periodEnd,quantity):
        '''
        Constructor
        '''
        self.initialize(service,periodStart,periodEnd,quantity)
        
    def initialize(self, service,periodStart,periodEnd,quantity):
        AbstractTrading.initialize(self, service,periodStart,periodEnd,quantity)