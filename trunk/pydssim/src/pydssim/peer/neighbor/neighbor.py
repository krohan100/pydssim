from pydssim.util.protected import Protected
from pydssim.util.decorator.public import public
from pydssim.util.logger import Logger
import uuid

class Neighbor(Protected,INeighbor):
    """
    Defines the module with objective the implementation of Neighbor class.

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 20/08/2009
    """
    def __init__(self,neighborPeer, id=uuid.uuid1()):
        """
        Constructor of class
        
        """
        self.initialize(neighborPeer,id)
        
    def initialize(self,neighborpeer,id):
        """
        Initialize the object.
        
        """
        self.__neighborPeer = neighborPeer
        self.__id = id
        Logger().resgiterLoggingInfo("Create Neighbor "+ self.__peer.getId())
        
    @public
    def getId(self):
        return self.__id
    
          
    @public
    def getNeighborpeer(self):
        return self.__neighborPeer
    
    @public
    def dispatchData(self, data):
        """
        Dispatches data to neighborPeer
        @param data: an object
        @type data: object
        @return: an object
        @rtype: object
        """
       
        return self.__neighborPeer.input(data)