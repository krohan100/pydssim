'''
Created on 24/04/2010

@author: Luiz Gustavo
'''

from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.peer.trading.abstract_trading import AbstractTrading
from pydssim.peer.service.shared_period import SharePeriod
from pydssim.util.log.trading_logger import TradingLogger
from pydssim.peer.history.history import History
import traceback

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
        
        TradingLogger().resgiterLoggingInfo("verify Trading ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingMetric,tradingQuantity,equivalenceEquivalenceResource, equivalenceEquivalenceUUID,sharePeriodMetric,equivalenceQuantityTrand,tradingDPeriodStart,tradingTPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd,sharePeriodDPeriodStart,sharePeriodTPeriodStart,sharePeriodDPeriodEnd,sharePeriodTPeriodEnd,tradingAttempt = data.split()
        
         
        # Put in History 
        
        history = History(peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingMetric,tradingQuantity,equivalenceEquivalenceResource,
                          equivalenceEquivalenceUUID,sharePeriodMetric,equivalenceQuantityTrand,tradingDPeriodStart,tradingTPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd)
        
        self.getTradingManager().getPeer().getHistoryResource().addElement(history)
        
        
        service = None
        print self.getTradingManager().getPeer().getServices().getElements().values()
        for service in self.getTradingManager().getPeer().getServices().getElements().values():
            
            if tradingServiceResource == service.getResource():
                break
        
             
        if not service:
            
            
            return False
        
        
        tradingPeriodStart = "%s %s"%(tradingDPeriodStart,tradingTPeriodStart)
        tradingPeriodEnd = "%s %s"%(tradingDPeriodEnd,tradingTPeriodEnd)
        
        # verify if service shared
        hasShare = service.hasSharePeriodswithQuantity(tradingPeriodStart,tradingPeriodEnd,tradingQuantity,tradingMetric)
        
        if not hasShare:
            return False
        
        #verificar quantidade 
        
        equivalenceRepository = self.getTradingManager().getPeer().getEquivalenceRepository()
        
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
        
        TradingLogger().resgiterLoggingInfo("send Tradind For Children ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        peerNeighbors = self.getTradingManager().getPeer().getPeerNeighbors()
        
       
        try:
            for host, port in peerNeighbors.values():
                 
                #self.getTradingManager().getPeer().getPeerLock().acquire()  
                print "enter", host,port,self.getTradingManager().getPeer().getPID()           
                resp = self.getTradingManager().getPeer().connectAndSend(host, int(port), AbstractMessageHandler.TRADINGCH,data)#[0]
                
                
                #self.getTradingManager().getPeer().getPeerLock().release()
        except:
            traceback.print_exc()
              
        
        return True     
        
    def sendTradindForSuperPeerNeighbor(self,data):
        
        TradingLogger().resgiterLoggingInfo("send Tradind For Super Peer Neighbor ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        peerNeighbors = self.getTradingManager().getPeer().getSuperPeerNeighbor()
        
        for super in peerNeighbors.keys():
            
            host, port = super.split(":")
      
            self.getTradingManager().getPeer().getPeerLock().acquire()             
            resp = self.getTradingManager().getPeer().connectAndSend(host, int(port), AbstractMessageHandler.TRADINGCSN,data)#[0]
            self.getTradingManager().getPeer().getPeerLock().release()
            
    def __consultEquivalenceAndShare(self,service,periodStart,periodEnd):
        
        TradingLogger().resgiterLoggingInfo("consult Equivalence And Share ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        sharePeriods = {}
        flag = True 
        equivalence = None
        
        serviceEquivalences = self.getTradingManager().getPeer().getEquivalenceRepository()
        
        serviceEquivalence = serviceEquivalences.getElementID(service.getUUID())
        
        #equivalencesInPeriod = serviceEquivalence.getAllEquivalenceInPeriod(periodStart,periodEnd)
        
        equivalencesInPeriod = serviceEquivalence.getEquivalences()
        
        if not equivalencesInPeriod:
            return (equivalence,sharePeriods)
        
               
        for equivalenceID, equivalence in equivalencesInPeriod.iteritems():
            
            equivalenceService = equivalence.getEquivalence()
            #sharePeriods = equivalenceService.getResourceS().hasSharePeriods(periodStart,periodEnd)
            sharePeriods = equivalenceService.getResourceS().getSharePeriod()
            
            
            if  sharePeriods:
                flag = False
                break
                
        if flag:
            #Pensar em criar uma opcao qduo nao tiver equivalaencia
            pass
            
        return (equivalence,sharePeriods)    
    
    def searchServiceForTrading(self,trading):
        
        TradingLogger().resgiterLoggingInfo("search Service For Trading ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        #if trading.getAttempt == 1:
        equivalence,sharePeriodsEquiva = self.__consultEquivalenceAndShare(trading.getService(), trading.getPeriodStart(), trading.getPeriodEnd())
        
        if not equivalence:
           
            return False
        
        quantityTrand = int((trading.getQuantity()*equivalence.getEquivalenceQuantity())/equivalence.getServiceQuantity())
        
        trading.setQuantityEquivalence(quantityTrand)
        trading.setEquivalence(equivalence)
        
        self.getTradingManager().getTradings().addElement(trading)
        
        sharePeriod  = None
        for shareID, sharePeriod in sharePeriodsEquiva.iteritems():
            if sharePeriod.getQuantity()>= quantityTrand and sharePeriod.getMetric() == trading.getMetric() and sharePeriod.getStatus() == SharePeriod.IDLE:
                sharePeriod.setStatus(SharePeriod.TRADING)
                break
                
        if not sharePeriod:
            return False
        
        
        
        superPeer = self.getTradingManager().getPeer().getMySuperPeer()
        peerSource      = self.getTradingManager().getPeer().getPID()
        
        TradingLogger().resgiterLoggingInfo("Send for SuperPeer = %s ,Peer = %s"%(superPeer,self.getTradingManager().getPeer().getPID()))
        
        
        hostSuper,portSuper = superPeer.split(":")
        
        
        
        
        msgSend = "%s %s %s %s %s %d %s %s %s %d %s %s %s %s %d"%(peerSource,trading.getUUID(),trading.getService().getResource(),trading.getService().getUUID(),trading.getMetric(),trading.getQuantity(),
                                          equivalence.getEquivalence().getResource(),equivalence.getEquivalence().getUUID(),sharePeriod.getMetric(),quantityTrand,trading.getPeriodStart(),
                                          trading.getPeriodEnd(),sharePeriod.getPeriodStart(),sharePeriod.getPeriodEnd(),trading.getAttempt())
           
        print msgSend   
        #self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(hostSuper, portSuper, AbstractMessageHandler.TRADINGSP,msgSend)#[0]
      
        #self.getTradingManager().getPeer().getPeerLock().release()
        
        return True
            
    def sendStartTrading(self,data):
        
        TradingLogger().resgiterLoggingInfo("send Start Trading ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingQuantity,equivalenceEquivalenceResource,
        equivalenceEquivalenceUUID,equivalenceQuantityTrand,tradingDPeriodStart,tradingtPeriodStart,tradingDPeriodEnd,
        tradingTPeriodEnd,sharePeriodPeriodStart,sharePeriodPeriodEnd,tradingAttempt = data.split()
        
       
        host,port = peerSource.split(":")
        
        msg = "%s %s"%(self.getTradingManager().getPeer().getPID(),tradingUUID)
        #self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGST,msg)#[0]
      
        #self.getTradingManager().getPeer().getPeerLock().release()
        
        peer,tradingUUID,responseTrand = resp[0][1]
        
        trading = self.__tradingManager.getTradings().getElementID(tradingUUID)
        
        trading.setStatus(responseTrand)
        
            
    def verifyTrust(self,data):
        
        TradingLogger().resgiterLoggingInfo("verify Trust ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
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
        
        print "enter", self.getTradingManager().getPeer().getPID()
        TradingLogger().resgiterLoggingInfo("send Response To Peer Winner ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        msg = "%s %s"%(trading.getUUID(),AbstractTrading.NOTCOMLETE,myPeer)
            
        host,port = peer.split(":")
        #self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCP,msg)#[0]
  
        #self.getTradingManager().getPeer().getPeerLock().release() 
        
        return resp[0][1]  
    
    def recvResponseToPeer(self,data):
        
        TradingLogger().resgiterLoggingInfo("recv Response To Peer ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        tradingUUID,status,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        
        #colocar uma verificacao#
        
        trading.setStatus(status)
        msg = AbstractTrading.NOTCOMLETE
        if status == AbstractTrading.COMPLETE:
            msg = AbstractTrading.ACK
            
        return msg 
                
    def sendOwnershipCertificate(self,trandig,myPeer,peer):
        
        print "enter OC", self.getTradingManager().getPeer().getPID()
        
        TradingLogger().resgiterLoggingInfo("send OwnershipCertificate ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        msg = "%s %s"%(trading.getUUID(),myPeer)
            
        host,port = peer.split(":")
        #self.getTradingManager().getPeer().getPeerLock().acquire()             
        resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGOC,msg)#[0]
  
        #self.getTradingManager().getPeer().getPeerLock().release() 
        
        return resp[0][1]   
                    
    def recvOwner(self, data):
        
        TradingLogger().resgiterLoggingInfo("recv Owner ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        tradingUUID,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        trading.setOwnershipCertificate(ownershipCertificate,trading.getService())
        
        
        
        
        
    def sendResponseToPeerAll(self,trading,myPeer,peer):
        
        TradingLogger().resgiterLoggingInfo("send Response To Peer All ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        for peerTrading in trading.getPeersTrading().keys():
                       
            if peerTrading == peer:
                continue
            
            msg = "%s %s"%(trading.getUUID(),AbstractTrading.NOTCOMLETE,myPeer)
                
            host,port = peerTrading.split(":")
            #self.getTradingManager().getPeer().getPeerLock().acquire()             
            resp = self.getTradingManager().getPeer().connectAndSend(host, port, AbstractMessageHandler.TRADINGCP,msg)#[0]
      
            #self.getTradingManager().getPeer().getPeerLock().release() 
           
                  
            
    def recvResponseToPeerComplete(self,data):
        
        print "enter Complete ", self.getTradingManager().getPeer().getPID()
        
        TradingLogger().resgiterLoggingInfo("recv Response To Peer Complete ,Peer = %s"%(self.getTradingManager().getPeer().getPID()))
        
        tradingUUID,status,myPeer = data.split()
        
        trading = self.getTradingManager().getTradings().getElementID(tradingUUID)
        

        
        trading.setStatus(status)
        msg = AbstractTrading.NULL
        if status == AbstractTrading.COMPLETE:
            msg = AbstractTrading.ACK
            
        return msg