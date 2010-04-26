'''
Created on 24/04/2010

@author: Luiz Gustavo
'''

from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler

class InformationServiceAgent(object):
    '''
    classdocs
    '''


    def __init__(self,tradingManager):
        '''
        Constructor
        '''
        
        self.__tradingManager = tradingManager
    
    def getTradingManager(self):
        return self.__tradingManager
    
    def sendTradindForChildren(self,data):
        
        peerNeighbors = self.getTradingManager().getPeer().getPeerNeighbors()
        
        for host, port in peerNeighbors.values():
      
      
            
            self.getTradingManager().getPeer().getPeerLock().acquire()             
            resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCH,data)#[0]
            self.getTradingManager().getPeer().getPeerLock().release()
        
        
        
    def __consultEquivalenceAndShare(self,service,periodStart,periodEnd,quantity):
        
        serviceEquivalences = self.getTrading().getPeer().getEquivalenceRepository()
        
        serviceEquivalence = serviceEquivalences.getElementID(service.getUUID())
        
        equivalencesInPeriod = serviceEquivalence.getAllEquivalenceInPeriod(periodStart,periodEnd)
        
        sharePeriods = {}
        flag = True        
        for equivalenceID, equivalence in equivalencesInPeriod.iteritems():
            
            equivalenceService = equivalence.getEquivalence()
            sharePeriods = equivalenceService.hasSharePeriods(periodStart,periodEnd)
            if  sharePeriods:
                flag = False
                break
                
        if flag:
            #Pensar em criar uma opcao qduo nao tiver equivalaencia
            pass
            
        return (equivalence,sharePeriods)    
            
        
    
    def searchServiceForTrading(self,trading):
        
        
        
        equivalence,sharePeriods = self.__consultEquivalenceAndShare(trading.getService(), trading.getPeriodStart(), trading.getPeriodEnd())
        
        quantityTrand = int((trading.getQuantity()*equivalece.getEquivalenceQuantity())/equivalence.getServiceQuantity())
        
        trading.setQuantityEquivalence(quantityTrand)
        trading.setEquivalence = equivalence
        
        for shareID, sharePeriod in sharedPeriods.iteritems():
            if sharePeriod.getQuantity()>= quantityTrand and sharePeriod.getStatus() == SharePeriod.IDLE:
                sharePeriod.setStatus(SharePeriod.TRADING)
                break
            
       
        superPeer = self.getTradingManager().getPeer().getMySuperPeer()
        peerSource      = self.getTradingManager().getPeer().getPID()
        
        hostSuper,portSuper = superPeer.split(":")
        
        
        
        
        msgSend = "%s %s %s %s %d %s %s %d %s %s"%(peerSource,trading.getUUID(),trading.getService().getResource(),trading.getService().getUUID(),trading.getQuantity(),
                                          equivalence.getEquivalence().getResource(),equivalence.getEquivalence().getUUID(),quantityTrand,
                                          sharePeriod.getPeriodStart(),sharePeriod.getPeriodEnd())
           
        print msgSend   
        self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(hostSuper, portSuper, AbstractMessageHandler.TRADINGSP,msgSend)#[0]
      
        self.getTradingManager().getPeer().getPeerLock().release()
        trustFinalValue = float(resp[0][1])
                
        
        
        
        

        
        