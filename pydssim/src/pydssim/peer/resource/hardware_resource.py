'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.resource.abstract_resource import AbstractResource
from pydssim.util.decorator.public import public
from random import randint
import uuid

class Hardware(AbstractResource):
    '''
    classdocs
    '''

    def __init__(self,pid ,resource='',size= randint(1,100000),sharePercente = randint(10,90),description='hardware',availabity=True,period={}):
        '''
        Constructor
        '''
        self.initialize(pid, resource,size,sharePercente,description,availabity,period)
       
        
    def initialize(self, pid,resource,size,sharePercente,description,availabity,period):
        
        AbstractResource.initialize(self, pid,resource,description,availabity,period)
        
        self.__size = size
        self.__shareSize = self.__size*(sharePercente/100)
        self.__quantity = sharePercente
        
    @public
    def getSize(self):
        return self.__size
    
    @public
    def getshareSize(self):
        return self.__shareSize   
    
    @public
    def getQuantity(self):
        return self.__quantity 
    
    @public
    def setSize(self,size):
        self.__size = size
        return self.__size
    
    @public
    def setshareSize(self,shareSize):
        self.__shareSize = shareSize
        return self.__shareSize   
    
    @public
    def getQuantity(self,quantity):
        self.__quantity = quantity
        return self.__quantity    
            
        