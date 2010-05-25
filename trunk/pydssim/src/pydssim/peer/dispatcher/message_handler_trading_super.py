'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.log.message_logger import MessageLogger
import traceback

class MessageHandlerTradingSuperPeer(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"TRADINGSP",AbstractMessageHandler.TRADINGSP)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the TRUSTFINAL message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            try:
                #print  data
                
                peerSource,tradingUUID,tradingServiceResource,tradingServiceUUID,tradingMetric,tradingQuantity,equivalenceEquivalenceResource, equivalenceEquivalenceUUID,sharePeriodMetric,equivalenceQuantityTrand,tradingDPeriodStart,tradingTPeriodStart,tradingDPeriodEnd,tradingTPeriodEnd,sharePeriodDPeriodStart,sharePeriodTPeriodStart,sharePeriodDPeriodEnd,sharePeriodTPeriodEnd,tradingAttempt = data.split()
                
                if int(tradingAttempt) ==1:               
                    self.getPeer().getTradingManager().getISA().sendTradindForChildren(data)
                else:
                    myPID = self.getPeer().getPID()
                    self.getPeer().getTradingManager().getISA().sendTradindForSuperPeerNeighbor(myPIDdata)    
                
                    #print "MTSP"
                MessageLogger().resgiterLoggingInfo('TRADINGSP %s %s: %s' % (self.getPeer().getPID(),str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.REPLY, self.getPeer().getPID())
                
                       
            except:
                
                MessageLogger().resgiterLoggingInfo('invalid TurstFinalValue %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()        
        finally:
            self.getPeer().getPeerLock().release()