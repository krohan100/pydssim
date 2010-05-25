'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.peer.dispatcher.abstract_message_handler import AbstractMessageHandler


class MessageHandlerPeerExit(AbstractMessageHandler):
    
    def __init__(self,peer ):
        self.initialize(peer,"PEEREXIT",AbstractMessageHandler.PEEREXIT)
        
    def executeHandler(self,peerConn,data):
        
        self.getPeer().getPeerLock().acquire()
        try:
            peerID = data.lstrip().rstrip()
            if peerID in self.getPeer().getpeerIDs():
                msg = 'Quit: peer removed: %s' % peerID 
                
                peerConn.sendData(AbstractMessageHandler.REPLY, msg)
                self.getPeer().removepeer(peerID)
            else:
                msg = 'Quit: peer not found: %s' % peerID 
                print msg
                peerConn.sendData(AbstractMessageHandler.ERROR, msg)
        finally:
            self.getPeer().getPeerLock().release()