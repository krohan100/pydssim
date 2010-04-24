'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.service.abstract_service import AbstractService
import uuid 

class Service(AbstractService):
    
    
    def __init__(self,pid ,resource='',description='service',availabity=True,period={}):
        '''
        Constructor
        '''
        self.initialize(pid, resource,description,availabity,period)
        
    def initialize(self, pid,resource,description,availabity,period):
        AbstractService.initialize(self, pid,resource,description,availabity,period)
            
    
    