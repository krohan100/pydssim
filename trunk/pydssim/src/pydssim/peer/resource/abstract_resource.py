'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''

from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public, createURN
import uuid

class AbstractResource():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, peer,resource, description='',availabity=True,period={}):
      
        self.__uuid = createURN(description)#uuid.uuid1()
        self.__resource = resource
        self.__description = description
        self.__peer = peer
        self.__availability = availabity
        self.__period = period
        
        
    @public    
    def getResource(self):
        return self.__resource
    
    @public
    def setResource(self,resource):
        self.__resource = resource
        return self.__resource
    
    @public 
    def getDescription(self):
        return self.__description
    
    @public
    def getPeer(self):
        return self.__peer
    
    @public
    def setPeer(self,peer):
        self.__peer = peer
        return self.__peer
    
    @public 
    def getAvailability(self):
        return self.__availability
    
    @public
    def getPeriod(self):
        return self.__period
    
    @public
    def getLocal(self):
        return self.__local
    
    @public
    def getUUID(self):
        return self.__uuid