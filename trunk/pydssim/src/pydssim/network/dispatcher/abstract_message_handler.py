from pydssim.util.logger import Logger

class AbstractMessageHandler():
    
    PEERNAME        = "0001"# request a peer's canonical id
    LISTPEERS       = "0002"
    LISTSPEERS      = "0003"   # List Super Peer
    INSERTPEER      = "0004"
    INSERTSPEER     = "0005"
    QUERY           = "0006"
    QRESPONSE       = "0007"
    FILEGET         = "0008"
    PEERQUIT        = "0009"
    SUPERPEER       = "0010"
    SSUPERPEER      = "0012"
    REPLY           = "0013"
    ERROR           = "0014"
    PEERFULL        = "0015"
    PEEREXIT        = "0016" 
    FIRSTSP         = "0017"
    UPDATEPEERLEVEL = "0018"
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self,  peer, messageName, canID):
        self.__messageName = messageName
        self.__peer = peer
        self.__canID = canID
        #Logger().resgiterLoggingInfo("Message => Create Message Handler %s can %s"%(self.__messageName,self.__canID))
                                     
    
    
    def getMessageName(self):
        return self.__messageName
    
    
    def getPeer(self):
        return self.__peer
    
  
    def getCanID(self):
        return self.__canID
    
        
    def executeHandler(self,peerConn,data):
        raise NotImplementedError()