'''
Created on 11/04/2010

@author: Luiz Gustavo
'''

import time
from pydssim.peer.repository.direct_trust_repository import DirectTrustRepository
from pydssim.peer.repository.trust_final_repository import TrustFinalRepository
from pydssim.util.data_util import strTime

class TrustManager(object):
    '''
    classdocs
    '''


    def __init__(self,peer):
        '''
        Constructor
        '''
        
        self.__directTrust= DirectTrustRepository(peer)
        self.__trustFinal = TrustFinalRepository(peer)
        
    def getDirectTrust(self):
        return self.__directTrust
    
    def getTrustFinal(self):
        return self.__trustFinal
    
    def getPeerService(self,peerID,service,startDate,StopDate):
        pass
        
        
    def directTrustCalculation(self,peerID,service,startDate,stopDate):
        
        peerConf  = 0.0
        rating    = 0.0
        nRating   = 0
        
        directTrusts = self.getDirectTrust().getElements()
        
        transaction = 0
        totalTransaction = 0
        sConfDir = 0.0
        
        print peerID,service,startDate,stopDate
        for key in directTrusts.keys():
            
            directTrust = directTrusts[key]
            
            if ((directTrust.getPeerUUID() == peerID) and (startDate<=directTrust.getPeriod()<=stopDate)):
                totalTransaction+=1
                if directTrust.getStatus() == True:
                    transaction +=1
                    if directTrust.getResourceDescription() == service:
                        nRating +=1
                        rating += directTrust.getRating()
                        
                
        if nRating != 0:        
            sConfDir = float(((transaction/totalTransaction)*(rating/nRating)))
        
        
        return sConfDir
    
    
    
        