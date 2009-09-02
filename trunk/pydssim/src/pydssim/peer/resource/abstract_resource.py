'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''

from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
import uuid

class AbstractResource(Protected):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, pid,resource, description='',availabity=True,period={}):
      
        self.__uuid = uuid.uuid1()
        self.__type = resource
        self.__description = description
        self.__pid = pid
        self.__availability = availabity
        self.__period = period
        

        
    @public    
    def getType(self):
        return self.__type
    
    @public 
    def getDescription(self):
        return self.__description
    
    @public
    def getPID(self):
        return self.__pid
    
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