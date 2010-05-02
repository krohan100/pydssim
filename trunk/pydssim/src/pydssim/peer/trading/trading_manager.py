'''
Created on 11/04/2010

@author: Luiz Gustavo
'''

import time
import threading
from pydssim.peer.trading.information_service_agent import InformationServiceAgent
#from pydssim.util.data_util import strTime
from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.peer.repository.tradings_repository import TradingsRepository
from pydssim.peer.trading.trading_service import TradingService
from pydssim.peer.trading.abstract_trading import AbstractTrading
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
        
        self.__peer = peer
        self.__tradings = TradingsRepository(peer)
        
    
    def getPeer(self):
        return self.__peer
        
    def getISA(self):
        return self.__isa
    
    def getTradings(self):
        return self.__tradings
    
    def creatTradingService(self,service,periodStart,periodEnd,quantity):
        
        trading = TradingService(service,periodStart,periodEnd,quantity)
        self.createTrading(trading)
        
        return trading
    
    def createTrading(self,trading):
        
        t = threading.Thread(target = setServiceForTrading,args=(trading))
        t.start()
    
    def setServiceForTrading(self,trading):
        
        self.getTradings().addElement(trading)
        self.__isa= InformationServiceAgent(self)
        self.__isa.searchServiceForTrading(trading)
        tradingUUID = trading.getUUID()
        while trading.getStatus == AbstractTrading.STARTED:
            
            trading = self.__tradingManager.getTradings().getElementID(tradingUUID)
            if trading.getStatus() == AbstractTrading.NOTCOMLETE:
                continue 
            
            
            peer,trust = trading.definyPeerTrading()
            
            if trust >= 0.5 or len(trading.getPeersTrading()>3):
                if self.__isa.sendResponseToPeerWinner(trandig,self.getPeer().getPID(),peer)== AbstractTrading.ACK:
                    trading.setStatus(AbstractTrading.COMPLETE)
                    ownershipCertificate = self.__isa.sendOwnershipCertificate(trandig,self.getPeer().getURN(),peer)
                    trading.setOwnershipCertificate(ownershipCertificate,trading.getEquivalence())
                else:
                    trading.getPeersTrading().pop(peer)    
                    
                
        self.__isa.sendResponseToPeerAll(trandig,self.getPeer().getPID(),peer)
                
        
        
        
        
        