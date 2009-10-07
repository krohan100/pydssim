"""
Defines the module with objective the implementation of Neighbor class.

@author: Luiz Gustavo
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 20/08/2009
"""


class INeighbor(object):
        
    def getId(self):
        """
        uuid Neighbor
        """
        raise NotImplementedError()
       
    def getNeighborpeer(self):
        raise NotImplementedError()
    
    def dispatchData(self, data):
        """
        Dispatches data to neighbor
        @param data: an object
        @type data: object
        @return: an object
        @rtype: object
        """
        raise NotImplementedError()