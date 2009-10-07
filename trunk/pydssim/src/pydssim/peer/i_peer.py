"""
Defines the module with the specification of IPeer interface.

@author: Luiz Gustavo
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 20/08/2009
"""

class IPeer(object):
    """
    Defines the interface of peer objects.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 20/08/2009
    """
      
    def __init__(self):
        raise NotImplementedError()
    
    def getId(self):
        raise NotImplementedError()
    
    def isConnected(self):
        raise NotImplementedError()
    
    def setProtocol(self):
        raise NotImplementedError()
    
    def getNetwork(self):
        raise NotImplementedError()
       
      
    def connected(self): 
        raise NotImplementedError()
    
    def disconnected(self):
        raise NotImplementedError()
             
    def receiveMessage(self, message):
        raise NotImplementedError()
    
    def sendMessage(self, message):
        raise NotImplementedError()
    
    def createConnection(self, targetId):
        raise NotImplementedError()
    
    def removeConnection(self, targetId):
        raise NotImplementedError()
            
    def setConnectionTime(self, time):
        raise NotImplementedError()
    
    def getConnectionTime(self):
        raise NotImplementedError()
    
    def getNeighbor(self, id):
        raise NotImplementedError()
    
    def getNeighbors(self):
        raise NotImplementedError()
    
    def addNeighbor(self, neighbor):
        raise NotImplementedError()
    
    def removeNeighbor(self, neighbor):
        raise NotImplementedError()
    
    def countNeighbor(self):
        raise NotImplementedError()
    
    def hasNeighbor(self, neighborId):
        raise NotImplementedError()
    
    def setDisconnectionTime(self, time):
        raise NotImplementedError()
    
    def getDisconnectionTime(self):
        raise NotImplementedError()
    
    def setScheduledForDisconnection(self, flag):
        raise NotImplementedError()
    
    def getScheduledForDisconnection(self):
        raise NotImplementedError()
    
    def getType(self):
        raise NotImplementedError()
    
    def setType(self):
        raise NotImplementedError()
    
    def input(self,  data):
        raise NotImplementedError()
    
    def output(self,  data):
        raise NotImplementedError()
    