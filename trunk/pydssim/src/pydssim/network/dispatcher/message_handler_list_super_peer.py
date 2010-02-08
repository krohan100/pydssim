'''
Created on 23/01/2010

@author: LGustavo
'''
from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.logger import Logger
import traceback

class MessageHandlerListSuperPeer(AbstractMessageHandler):
    
    def __init__(self,peer):
        self.initialize(peer,"LISTSPEERS",AbstractMessageHandler.LISTSPEERS)
        
    def executeHandler(self,peerConn,data):
        
        """ Handles the LISTSPEERS message type. Message data is not used. """

        self.getPeer().getPeerLock().acquire()
        try:
            try:
                
                if self.getPeer().numberOfSuperPeers() > 0:
                    
                    peerConn.sendData(AbstractMessageHandler.REPLY, '%d' % self.getPeer().numberOfSuperPeers())
                    for pid in self.getPeer().getSuperPeerIDs():
                        host,port = pid.split(":")
                        
                        peerConn.sendData(AbstractMessageHandler.REPLY, '%s %s %s' % (pid, host, port))
                else:
                    
                    peerConn.sendData(AbstractMessageHandler.FIRSTSP, '%d'%self.getPeer().numberOfSuperPeers())
                        
            except:
                
                Logger().resgiterLoggingInfo('invalid List Super Peer %s: %s' % (str(peerConn), data))
                peerConn.sendData(AbstractMessageHandler.ERROR, 'Join: incorrect arguments')
                traceback.print_exc()        
        finally:
            self.getPeer().getPeerLock().release()