"""
Defines the module with the implementation AbstractPeer class.

@author: Luiz Gustavo 
@organization: Federal University of Rio de Janeiro
@contact: lglmoura@cos.ufrj.br 
@since: 28/10/2009
"""

from pydssim.peer.abstract_peer import AbstractPeer
from pydssim.util.decorator.public import public,createURN

class DefaultPeer(AbstractPeer):
    """
    Implements the basic functions of a peer.
    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self,network, pid=createURN("peer")):
        
        AbstractPeer.initialize(self,  network, pid)
    
    

        