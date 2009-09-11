'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.resource.abstract_resource import AbstractResource
import uuid 

class Service(AbstractResource):
    
    
    def __init__(self,pid=uuid.uuid1() ,resource='',description='Service',availabity=True,period={}):
        '''
        Constructor
        '''
        self.initialize(pid, resource,description,availabity,period)
        
    def initialize(self, pid,resource,description,availabity,period):
        AbstractResource.initialize(self, pid,resource,description,availabity,period)
            
    
    