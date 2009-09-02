'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.util.decorator.public import public
from random import randint

class Hardware(AbstractResource):
    '''
    classdocs
    '''

    def __init__(self,pid ,resource,maxRange= 100000,sharePercente = 50,description='',availabity=True,period={}):
        '''
        Constructor
        '''
        self.initialize(pid, resource,maxRange,sharePercente,description,availabity,period)
       
        
    def initialize(self, pid,resource,maxRange,sharePercente,description,availabity,period):
        
        AbstractResource.initialize(self, pid,resource)
        
        self.__size = randint(0,maxRange)
        self.__shareSize = self.__size*(sharePercente/100)
        self.__quantity = sharePercente
        
    @public
    def getSize(self):
        return self.__size
    
    @public
    def getshareSize(self):
        return self.__shareSize        
            
        