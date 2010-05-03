'''
Created on 24/04/2010

@author: Luiz Gustavo
'''

from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.peer.trading.abstract_trading import AbstractTrading

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
    
    def verifyTrading(self,data):
        
        peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingQuantity,equivalenceEquivalenceResource,
        equivalenceEquivalenceUUID,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,
        tradingTPeriodEnd,sharePeriodPeriodStart,sharePeriodPeriodEnd,tradingAttempt = data.split()
        
        
        # Put in History 
        
        history = History(peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingMetric,tradingQuantity,equivalenceEquivalenceResource,
                          equivalenceEquivalenceUUID,euqivalenceMetric,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd)
        
        self.getTrading().getPeer().getHistoryResource().AddElement(history)
        
        
        # Search for service
        for service in self.getTrading().getPeer().getServices().getElements().values():
            
            if tradingServiceResource == service.getResource():
                break
            
        if not service:
           return False
        
        tradingPeriodStart = "%s %s"%(tradingDPeriodStart,tradingTPeriodStart)
        tradingPeriodEnd = "%s %s"%(tradingDPeriodEnd,tradingTPeriodEnd)
        
        # verify if service shared
        hasShare = service.hasSharePeriodswithQuantity(self,tradingPeriodStart,tradingPeriodEnd,tradingQuantity,tradingMetric)
        
        if not hasShare:
            return False
        
        #verificar quantidade 
        
        equivalenceRepository = self.getTrading().getPeer().getEquivalenceRepository()
        
        serviceEquivalent  = equivalenceRepository.getElementID(service.getUUID())
        
        hasEquiv = serviceEquivalent.hasEquivalencesForTag(equivalenceEquivalenceResource,periodStart,periodEnd)
               
        if not hasEquiv:
            return False
        
        trust = self.getTradingManager().getPeer().getTrustManager().TrustFinalValueCalculation(peerSource,
                                                                                                tradingServiceResource,
                                                                                                tradingPeriodStart,
                                                                                                tradingPeriodEnd) 
        
        
        equivalenceID,equivalence = hasEquiv.popitem()
        
        trading = self.getTradingManager().creatTradingService(tradingServiceResource,tradingPeriodStart,tradingPeriodEnd,tradingQuantity)
        trading.setUUID(tradingUUID)
        
        trading.setQuantityEquivalence(equivalenceQuantityTrand)
        trading.setEquivalence(equivalence)
        trading.addPeerTrading(peerSource,trust)
        
        self.getTradingManager().getTradings().addElemt(trading)
        
        return True        
               
        

    
    def sendTradindForChildren(self,data):
        
        peerNeighbors = self.getTradingManager().getPeer().getPeerNeighbors()
        
        for host, port in peerNeighbors.values():
      
            self.getTradingManager().getPeer().getPeerLock().acquire()             
            resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCH,data)#[0]
            self.getTradingManager().getPeer().getPeerLock().release()
      
        
    def sendTradindForSuperPeerNeighbor(self,data):
        
        peerNeighbors = self.getTradingManager().getPeer().getSuperPeerNeighbor()
        
        for super in peerNeighbors.keys():
            
            host, port = super.split(":")
      
            self.getTradingManager().getPeer().getPeerLock().acquire()             
            resp = self.getTradingManager().getPeer().connectAndSend(host, int(port), AbstractMessageHandler.TRADINGCSN,data)#[0]
            self.getTradingManager().getPeer().getPeerLock().release()
            
    def __consultEquivalenceAndShare(self,service,periodStart,periodEnd):
        
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
            
    def sendStartTrading(self,data):
        
        peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingQuantity,equivalenceEquivalenceResource,
        equivalenceEquivalenceUUID,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,
        tradingTPeriodEnd,sharePeriodPeriodStart,sharePeriodPeriodEnd,tradingAttempt = data.split()
        
       
        host,port = peerSource.split(":")
        
        msg = "%s %s"%(self.getTradingManager().getPeer().getPID(),tradingUUID)
        self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGST,msg)#[0]
      
        self.getTradingManager().getPeer().getPeerLock().release()
        
        peer,tradingUUID,responseTrand = resp[0][1]
        
        trading = self.__tradingManager.getTradings().getElementID(tradingUUID)
        
        trading.setStatus(responseTrand)
        
            
    def verifyTrust(self,data):
        
        peer,tradingUUID = data.split()
        
        trading = self.__tradingManager.getTradings().getElementID(tradingUUID)
        
        
        if trading.getStatus() == AbstractTrading.STARTED:
                
            trust = self.getTradingManager().getPeer().getTrustManager().TrustFinalValueCalculation(peer,
                                                                                                    trading.getService().getTag(),
                                                                                                    trading.getPeriodStart(),
                                                                                                    trading.getPeriodEnd()) 
            trading.addPeerTrading(peer,trust)
            
        return "%s %s"%(data,trading.getStatus())    
            
        
    def sendResponseToPeerWinner(self,trandig,myPeer,peer):
        
       
        msg = "%s %s"%(trading.getUUID(),AbstractTrading.NOTCOMLETE,myPeer)
            
        host,port = peer.split(":")
        self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCP,msg)#[0]
  
        self.getTradingManager().getPeer().getPeerLock().release() 
        
        return resp[0][1]  
    
    def recvResponseToPeer(self,data):
        
        tradingUUID,status,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        
        #colocar uma verificacao#
        
        trading.setStatus(status)
        msg = AbstractTrading.NOTCOMLETE
        if status == AbstractTrading.COMPLETE:
            msg = AbstractTrading.ACK
            
        return msg 
                
    def sendOwnershipCertificate(self,trandig,myPeer,peer):
        
        msg = "%s %s"%(trading.getUUID(),myPeer)
            
        host,port = peer.split(":")
        self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGOC,msg)#[0]
  
        self.getTradingManager().getPeer().getPeerLock().release() 
        
        return resp[0][1]   
                    
    def recvOwner(self, data):
        
        tradingUUID,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        trading.setOwnershipCertificate(ownershipCertificate,trading.getService())
        
        
        
        
        
    def sendResponseToPeerAll(self,trandig,myPeer,peer):
        
        for peerTrading in trading.getPeersTrading.keys():
                       
            if peerTrading == peer:
                continue
            
            msg = "%s %s"%(trading.getUUID(),AbstractTrading.NOTCOMLETE,myPeer)
                
            host,port = peerTrading.split(":")
            self.getTradingManager().getPeer().getPeerLock().acquire()             
            resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCP,msg)#[0]
      
        self.getTradingManager().getPeer().getPeerLock().release() 
           
                  
            
    def recvResponseToPeerComplete(self,data):
        
        tradingUUID,status,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        

        
        trading.setStatus(status)
        msg = AbstractTrading.NULL
        if status == AbstractTrading.COMPLETE:
            msg = AbstractTrading.ACK
            
        return msg
        
        
    def searchServiceForTrading(self,trading):
        
        #if trading.getAttempt == 1:
        equivalence,sharePeriodsEquiva = self.__consultEquivalenceAndShare(trading.getService(), trading.getPeriodStart(), trading.getPeriodEnd())[0]
        
        quantityTrand = int((trading.getQuantity()*equivalece.getEquivalenceQuantity())/equivalence.getServiceQuantity())
        
        trading.setQuantityEquivalence(quantityTrand)
        trading.setEquivalence(equivalence)
        
        self.getTradingManager().getTradings().AddElemts(trading)
        
        for shareID, sharePeriod in sharedPeriodsEquiva.iteritems():
            if sharePeriod.getQuantity()>= quantityTrand and sharePeriod.getMetric() == trading.getMetric() and sharePeriod.getStatus() == SharePeriod.IDLE:
                sharePeriod.setStatus(SharePeriod.TRADING)
                break
                
       
        superPeer = self.getTradingManager().getPeer().getMySuperPeer()
        peerSource      = self.getTradingManager().getPeer().getPID()
        
        hostSuper,portSuper = superPeer.split(":")
        
        
        
        
        msgSend = "%s %s %s %s % s%d %s %s %s %d %s %s %s %s %d"%(peerSource,trading.getUUID(),trading.getService().getResource(),trading.getService().getUUID(),trading.getMetric(),trading.getQuantity(),
                                          equivalence.getEquivalence().getResource(),equivalence.getEquivalence().getUUID(),sharePeriod.getMetric(),quantityTrand,trading.getPeriodStart(),
                                          trading.getPeriodEnd(),sharePeriod.getPeriodStart(),sharePeriod.getPeriodEnd(),trading.getAttempt())
           
        print msgSend   
        self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(hostSuper, portSuper, AbstractMessageHandler.TRADINGSP,msgSend)#[0]
      
        self.getTradingManager().getPeer().getPeerLock().release()
        
                
        
        
        
        

        
        