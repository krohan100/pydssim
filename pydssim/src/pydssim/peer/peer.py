#!/usr/bin/python

# btpeer.py

import socket
import struct
import threading
import time
import traceback
from peer_connection import PeerConnection

def debug( msg ):
    """ Prints a messsage to the screen with the name of the current thread """
    print "[%s] %s" % ( str(threading.currentThread().getName()), msg )


class Peer:
    """ Implements the core functionality that might be used by a peer in a
    P2P network.

    """


    
    def __init__( self, maxNeighbor=7, port=3000, id=None ):
   
    	""" Initializes a peer servent (sic.) with the ability to catalog
    	information for up to maxneighbors number of neighbors (maxneighbors may
    	be set to 0 to allow unlimited number of neighbors), listening on
    	a given server port , with a given canonical peer name (id)
    	and host address. 
    
    	"""
    	self.debug = 0
    
    	self.__maxNeighbor = maxNeighbor
    	self.__port = port
    	self.__host = socket.gethostbyname(socket.gethostname())
    
    	if id:
            self.__id = id
    	else: 
            self.id = '%s:%d' % (self.host, self.port)
    
    	self.__peerLock = threading.Lock()  
    	self.neighbors = {}        
    	self.shutdown = False  
    
    	self.handlers = {}
    	self.router = None


    def __debug( self, msg ):
    
    	if self.debug:
    	    btdebug( msg )

  
    def __handlePeer( self, clientSock ):
    
    	"""
    	handlepeer( new socket connection ) -> ()
    
    	Dispatches messages from the socket connection
    	"""
    
    	self.__debug( 'New child ' + str(threading.currentThread().getName()) )
    	self.__debug( 'Connected ' + str(clientsock.getPeerName()) )
    
    	host, port = clientSock.getPeerName()
    	peerConn = PeerConnection( None, host, port, clientSock, debug=False )
    	
    	try:
    	    msgType, msgData = peerConn.recvData()
    	    if msgType: msgType = msgType.upper()
    	    if msgType not in self.handlers:
    		self.__debug( 'Not handled: %s: %s' % (msgType, msgData) )
    	    else:
    		self.__debug( 'Handling peer msg: %s: %s' % (msgType, msgData) )
    		self.handlers[ msgType ]( peerConn, msgData )
    	except KeyboardInterrupt:
    	    raise
    	except:
    	    if self.debug:
    		traceback.print_exc()
    	
    	self.__debug( 'Disconnecting ' + str(clientSock.getPeerName()) )
    	peerConn.close()

    
    def __runStabilizer( self, stabilizer, delay ):
    
    	while not self.shutdown:
    	    stabilizer()
    	    time.sleep( delay )

	  
    def setId( self, id ):
    
	       self.id = id

  
    def startStabilizer( self, stabilizer, delay ):
    
    	""" Registers and starts a stabilizer function with this peer. 
    	The function will be activated every <delay> seconds. 
    
    	"""
    	t = threading.Thread( target = self.__runStabilizer, 
    			      args = [ stabilizer, delay ] )
    	t.start()

	

    
    def addHandler( self, msgType, handler ):
    
    	""" Registers the handler for the given message type with this peer """
    	assert len(msgType) == 4
    	self.handlers[ msgType ] = handler



   
    def addRouter( self, router ):
    
    	""" Registers a routing function with this peer. The setup of routing
    	is as follows: This peer maintains a list of other known neighbors
    	(in self.neighbors). The routing function should take the name of
    	a peer (which may not necessarily be present in self.neighbors)
    	and decide which of the known neighbors a message should be routed
    	to next in order to (hopefully) reach the desired peer. The router
    	function should return a tuple of three values: (next-peer-id, host,
    	port). If the message cannot be routed, the next-peer-id should be
    	None.
    
    	"""
    	self.router = router



   
    def addPeer( self, peerId, host, port ):
    
    	""" Adds a peer name and host:port mapping to the known list of neighbors.
    	
    	"""
    	if peerId not in self.neighbors and (self.maxNeighbors == 0 or len(self.neighbors) < self.maxNeighbors):
    	    self.neighbors[ peerid ] = (host, int(port))
    	    return True
    	else:
    	    return False



    
    def getPeer( self, peerId ):
    
    	""" Returns the (host, port) tuple for the given peer name """
    	assert peerId in self.neighbors    # maybe make this just a return NULL?
    	return self.neighbors[ peerId ]



    
    def removePeer( self, peerId ):
    
    	""" Removes peer information from the known list of neighbors. """
    	if peerId in self.neighbors:
    	    del self.neighbors[ peerId ]



    
    def addPeerAt( self, loc, peerId, host, port ):
    
    	""" Inserts a peer's information at a specific position in the 
    	list of neighbors. The functions addpeerat, getpeerat, and removepeerat
    	should not be used concurrently with addpeer, getpeer, and/or 
    	removepeer. 
    
    	"""
    	self.neighbors[ loc ] = (peerId, host, int(port))



    
    def getPeerAt( self, loc ):
    
    	if loc not in self.neighbors:
    	    return None
    	return self.neighbors[ loc ]



    
    def removePeerAt( self, loc ):
    
	       removePeer( self, loc ) 



    
    def getPeerIds( self ):
    
    	""" Return a list of all known peer id's. """
    	return self.neighbors.keys()


    def numberNeighbors( self ):
   
    	""" Return the number of known peer's. """
    	return len(self.neighbors)
 
    def maxNeighborsReached( self ):
       
    	""" Returns whether the maximum limit of names has been added to the
    	list of known neighbors. Always returns True if maxneighbors is set to
    	0.
    
    	"""
    	assert self.maxNeighbors == 0 or len(self.neighbors) <= self.maxNeighbors
    	return self.maxNeighbors > 0 and len(self.neighbors) == self.maxNeighbors


    def makeServerSocket( self, port, backlog=5 ):
  
    	""" Constructs and prepares a server socket listening on the given 
    	port.
    
    	"""
    	sockP = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    	sockP.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    	sockP.bind( ( '', port ) )
    	sockP.listen( backlog )
    	return sockP


    def sendToPeer( self, peerId, msgType, msgData, waitreply=True ):
   
    	"""
    	sendtopeer( peer id, message type, message data, wait for a reply )
    	 -> [ ( reply type, reply data ), ... ] 
    
    	Send a message to the identified peer. In order to decide how to
    	send the message, the router handler for this peer will be called.
    	If no router function has been registered, it will not work. The
    	router function should provide the next immediate peer to whom the 
    	message should be forwarded. The peer's reply, if it is expected, 
    	will be returned.
    
    	Returns None if the message could not be routed.
    	"""
    
    	if self.router:
    	    nextPid, host, port = self.router( peerId )
    	if not self.router or not nextPid:
    	    self.__debug( 'Unable to route %s to %s' % (msgType, peerId) )
    	    return None
    	#host,port = self.neighbors[nextpid]
    	return self.connectAndSend( host, port, msgType, msgData,
    				    pid=nextPid,
    				    waitreply=waitreply )
    


   
    def connectAndSend( self, host, port, msgType, msgData, 
			pid=None, waitreply=True ):
   
    	"""
    	connectandsend( host, port, message type, message data, peer id,
    	wait for a reply ) -> [ ( reply type, reply data ), ... ]
    
    	Connects and sends a message to the specified host:port. The host's
    	reply, if expected, will be returned as a list of tuples.
    
    	"""
    	msgReply = []
    	try:
    	    peerConn = PeerConnection( pid, host, port, debug=self.debug )
    	    peerConn.sendData( msgType, msgData )
    	    self.__debug( 'Sent %s: %s' % (pid, msgType) )
    	    
    	    if waitreply:
        		oneReply = peerConn.recvData()
        		while (oneReply != (None,None)):
        		    msgReply.append( oneReply )
        		    self.__debug( 'Got reply %s: %s' 
        				  % ( pid, str(msgReply) ) )
        		    oneReply = peerConn.recvData()
    	    peerConn.close()
    	except KeyboardInterrupt:
    	    raise
    	except:
    	    if self.debug:
    		traceback.print_exc()
    	
    	return msgReply

  
    
    def checkLiveNeighbors( self ):
    
    	""" Attempts to ping all currently known neighbors in order to ensure that
    	they are still active. Removes any from the peer list that do
    	not reply. This function can be used as a simple stabilizer.
    
    	"""
    	todelete = []
    	for pid in self.neighbors:
    	    isconnected = False
    	    try:
        		self.__debug( 'Check live %s' % pid )
        		host,port = self.neighbors[pid]
        		peerConn = PeerConnection( pid, host, port, debug=self.debug )
        		peerConn.sendData( 'PING', '' )
        		isconnected = True
    	    except:
                todelete.append( pid )
    	    if isconnected:
                peerConn.close()
    
    	self.peerlock.acquire()
    	try:
    	    for pid in todelete: 
                if pid in self.neighbors:
                    del self.neighbors[pid]
    	finally:
    	    self.peerlock.release()
        # end checkliveneighbors method



   
    def mainLoop( self ):
    
    	s = self.makeServerSocket( self.__port )
    	s.settimeout(2)
    	self.__debug( 'Server started: %s (%s:%d)'
    		      % ( self.id, self.host, self.port ) )
    	
    	while not self.shutdown:
            #print "Server started: %s (%s:%d)"%(self.myid, self.serverhost, self.serverport)
    	    try:
        		self.__debug( 'Listening for connections...' )
               
        		clientSock, clientAddr = s.accept()
        		clientSock.settimeout(None)
        
        		t = threading.Thread( target = self.__handlepeer,
        				      args = [ clientSock ] )
        		t.start()
    	    except KeyboardInterrupt:
    		print 'KeyboardInterrupt: stopping mainloop'
    		self.shutdown = True
    		continue
    	    except:
    		if self.debug:
    		    traceback.print_exc()
    		    continue
    
    	# end while loop
    	self.__debug( 'Main loop exiting' )
    
    	s.close()

