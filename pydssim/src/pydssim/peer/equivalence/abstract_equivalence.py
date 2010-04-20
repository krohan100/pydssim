'''
Created on 28/08/2009

@author: LGustavo

COLOCAR PARA LE DE ARQUIVO YAAM

'''


from pydssim.util.decorator.public import  createURN
from pydssim.util.data_util import randomDate
from random import random,randint
from pydssim.util.log.equivalence_logger import EquivalenceLogger


class AbstractEquivalence():
    '''
    classdocs
    '''
    
    SERVICE = "SERVICE"
    EQUIVALENCE = "EQUIVALENCE"

    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def initialize(self, resourceUUID, resourceDescription , equivalenceType= SERVICE , period = randomDate("1/1/2010 1:30", "1/12/2010 4:50", random())):
      
        self.__uuid = createURN("equivalence")
        self.__resourceUUID = resourceUUID
        self.__resourceDescription = resourceDescription
        self.__equivalenceType = equivalenceType
        self.__equivalences = {}
        
        
        
        
        EquivalenceLogger().resgiterLoggingInfo("Initialize Trust = URN = %s,Peer = %s ,Time %s, Description = %s rating = %f and status = %s"%(self.__uuid,self.__peerUUID,self.__period,self.__resourceDescription,self.__rating,self.__status))
     
        
    def getResourceDescription(self):
        return self.__resourceDescription 
      
    def getResourceUUID(self):
        return self.__resourceUUID
    
    def setResourceUUID(self,resource):
        self.__resourceUUID = resourceUUID
        return self.__resourceUUID
    
    def getEquivalences(self):
        return self.__equivalences
    
    def getequivalenceType(self):
        return self.__equivalenceType
       
    def getUUID(self):
        return self.__uuid
    
    def addEquivalence(self, equivalence):
        key = equivalence.getUUID()
        if not self.__equivalences.has_key(key):
            self.__equivalences[key] = equivalence
        
        RepositoryLogger().resgiterLoggingInfo("Add Service %s  in Repository URN  %s of peer %s "%(equivalence.getUUID(),self.__class__.__name__,self.__peer.getURN()))
        return equivalence
    
    
    def removeEquivalence(self, equivalence):
        key = equivalence.getUUID()
        if not self.__equivalences.has_key(key):
            raise StandardError()
        if self.__equivalences[key] > 0:
            del self.__equivalences[equivalence]
            
        return equivalence
    
    def lookForEquivalence(self,uuid):
        pass
    
    def countEquivalences(self):
        return len(self.__equivalences)
    
   
    def getEquivalences(self):
        return self.__elements