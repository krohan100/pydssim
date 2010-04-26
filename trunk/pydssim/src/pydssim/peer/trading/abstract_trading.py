'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''


from pydssim.util.decorator.public import  createURN
from pydssim.util.data_util import randomDate
from random import random,randint
from pydssim.util.log.trust_logger import TrustLogger


class AbstractTrading():
    '''
    classdocs
    '''
    STARTED = 1
    COMPLETE = 2
    NOTCOMLETE = 3
    NULL   = 0
  
    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, service,periodStart,periodEnd,quantity):
      
        self.__uuid = createURN("trading")
        self.__service = service
        self.__periodStart = periodStart
        self.__periodEnd = periodEnd
        self.__quantity = quantity
        self.__status   = AbstractTrading.STARTED
         
        
        TradingLogger().resgiterLoggingInfo("Initialize Trading = URN = %s,"%(self.__uuid))
     
    
    def setEquivalence(self,equivalence):
        self.__equivalence = equivalence
        
    def getEquivalence(self):
        return self.__equivalence
    
    def setQuantityEquivalence(self,quantity):
        self.__quantityEquivalnce = quantity
        
    def getQuantityEquvalence(self):
        return self.__quantityEquivalnce    
        
        
    def getUUID(self):
        return self.__uuid 
    
      
    def getService(self):
        return self.__service
    
    def getPeriodStart(self):
        return self.__periodStart
    
    def getPeriodEnd(self):
        return self.__periodEnd
    
    def getPeriods(self):
        return (self.__periodStart,self.__periodEnd)
    
    def getQuantity(self):
        return self.__quantity
    
    def getStatus(self):
        return self.__status
     