'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''


from pydssim.util.decorator.public import  createURN


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
      
        self.__uuid = createURN(description)
        self.__resource = resource
        self.__description = description
        self.__peer = peer
        self.__availability = availabity
        self.__period = period
        
   
        
        
       
    def getResource(self):
        return self.__resource
    
    
    def setResource(self,resource):
        self.__resource = resource
        return self.__resource
    
     
    def getDescription(self):
        return self.__description
    
    
    def getPeer(self):
        return self.__peer
    
    
    def setPeer(self,peer):
        self.__peer = peer
        return self.__peer
    
     
    def getAvailability(self):
        return self.__availability
    
    
    def getPeriod(self):
        return self.__period
    
    
    def getLocal(self):
        return self.__local
    
    
    def getUUID(self):
        return self.__uuid
    
    