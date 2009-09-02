'''
Created on 29/08/2009

@author: LGustavo
'''

from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public

class SharedResource(Protected):
    '''
    classdocs
    '''


    def __init__(self,resource,owner,period):
        '''
        Constructor
        '''
        self.__resource = resource
        self.__ownerCertificate = owner
        self.__period = period
        
    @public    
    def getOwnerCertificate(self):
        return self.__ownershipCertificate
    
    @public 
    def getResource(self):
        return self.__resource
    
    @public
    def getPeriod(self):
        return self.__period
        
        
        