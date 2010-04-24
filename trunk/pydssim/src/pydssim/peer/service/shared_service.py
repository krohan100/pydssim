'''
Created on 29/08/2009

@author: LGustavo
'''

class SharedService():
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
        
       
    def getOwnerCertificate(self):
        return self.__ownershipCertificate
    
   
    def getResource(self):
        return self.__resource
    
    
    def getPeriod(self):
        return self.__period
        
        
        