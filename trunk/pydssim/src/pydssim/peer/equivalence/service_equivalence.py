'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.peer.equivalence.abstract_equivalence import AbstractEquivalence


class ServiceEquivalence(AbstractEquivalence):
    
    
    def __init__(self,resource ):
        '''
        Constructor
        period = randomDate("1/1/2010 1:30", "1/12/2010 4:50", random())
        
        '''
        
        self.initialize(resource)
        
    def initialize(self, resource):
        AbstractEquivalence.initialize(self,resource)
            
    
    