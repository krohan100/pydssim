from pydssim.util.logger import Logger

class AbstractMessageHandler():
    
    PEERNAME    = "NAME"   # request a peer's canonical id
    LISTPEERS   = "LISP"
    LISTSPEERS  = "LISS"   # List Super Peer
    INSERTPEER  = "JOIN"
    INSERTSPEER = "SJIN"
    QUERY       = "QUER"
    QRESPONSE   = "RESP"
    FILEGET     = "FGET"
    PEERQUIT    = "QUIT"
    SUPERPEER   = "SUPE"
    SSUPERPEER  = "SSUP"
    REPLY       = "REPL"
    ERROR       = "ERRO"
    PEERFULL    = "PEFU"
    PEEREXIT    = "EXIT" 
    FIRSTSP     = "FTST"
    
    def __init__(self):
        raise NotImplementedError()
    
    def initialize(self,  peer, messageName, canID):
        self.__messageName = messageName
        self.__peer = peer
        self.__canID = canID
        Logger().resgiterLoggingInfo("Message => Create Message Handler %s can %s"%(self.__messageName,self.__canID))
                                     
    
    
    def getMessageName(self):
        return self.__messageName
    
    
    def getPeer(self):
        return self.__peer
    
  
    def getCanID(self):
        return self.__canID
    
        
    def executeHandler(self,peerConn,data):
        raise NotImplementedError()