
from pydssim.util.decorator.public import  createURN
from pydssim.util.logger import Logger
from pydssim.peer.neighbor.i_neighbor import INeighbor


class Neighbor(INeighbor):
    
    """
    Defines the module with objective the implementation of Neighbor class.

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 20/08/2009
    """
    
    def __init__(self,neighborPeer, id=createURN("neighbor")):
        """
        Constructor of class
        
        """
        self.initialize(neighborPeer,id)
        
    def initialize(self,neighborPeer,id):
        """
        Initialize the object.
        
        """
        self.__neighborPeer = neighborPeer
        self.__id = id
        Logger().resgiterLoggingInfo("Create Neighbor "+ self.__neighborPeer.getPID())
        
   
    def getId(self):
        return self.__id
    
          
   
    def getNeighborPeer(self):
        return self.__neighborPeer
    
    
    def dispatchData(self, data):
        """
        Dispatches data to neighborPeer
        @param data: an object
        @type data: object
        @return: an object
        @rtype: object
        """
       
        return self.__neighborPeer.input(data)