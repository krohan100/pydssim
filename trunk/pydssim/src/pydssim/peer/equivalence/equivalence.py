'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.equivalence.abstract_equivalence import AbstractEquivalence


class Equivalence(AbstractEquivalence):
    
    
    def __init__(self,pid ,resourceID,serviceQuantity,period, status):
        '''
        Constructor
        '''
        self.__period = period
        self.__serviceQuantity = serviceQuantit 
        self.initialize(pid, resource,resourceDescription , trustType,rating,period,status)
        
    def initialize(self, pid,resource,resourceDescription,trustType,rating,period,status):
        AbstractTrust.initialize(self, pid,resource,resourceDescription,trustType,rating,period,status)
            
    
    