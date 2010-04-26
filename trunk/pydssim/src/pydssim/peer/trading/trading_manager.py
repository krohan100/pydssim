'''
Created on 11/04/2010

@author: Luiz Gustavo
'''

import time
from pydssim.peer.trading.information_service_agent import InformationServiceAgent
#from pydssim.util.data_util import strTime
from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.peer.repository.tradings_repository import TradingsRepository
from random import random
from datetime import datetime


class TradingManager(object):
    '''
    classdocs
    '''


    def __init__(self,peer):
        '''
        Constructor
        '''
        
        self.__isa= InformationServiceAgent(self)
        
        self.__peer = peer
        self.__tradings = TradingsRepository(peer)
        
    
    def getPeer(self):
        return self.__peer
        
    def getISA(self):
        return self.__isa
    
    def getTradings(self):
        return self.__tradings
    
    def setServiceForTrading(self,service,periodStart,periodEnd,quantity):
        
        trading = TradingService(service,periodStart,periodEnd,quantity)
        self.getTradings().addElement(trading)
        