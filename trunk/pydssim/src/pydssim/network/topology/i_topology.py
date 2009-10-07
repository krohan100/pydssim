
class ITopology(object):
   
    """
    Defines the operations of Network topology.

    @author: Luiz Gustavo
    @organization: Federal University of Rio de Janeiro
    @contact: lglmoura@cos.ufrj.br 
    @since: 22/08/2009
    """

    def __init__(self):
        raise NotImplementedError()
    
    def addNeighbor(self, sourceId, targetId):
        """
        Creates a connection between two peers.
        @param sourceId: the identifier of source peer
        @type sourceId: int
        @param targetId: the identifier of target peer
        @type targetId: int
        @return: If connection was created, returns True. Else, returns False.
        @rtype: bool
        """
        raise NotImplementedError()
    
    def removeNeighbor(self, sourceId, targetId):
        """
        Removes a connection between two peers.
        @param sourceId: the identifier of source peer
        @type sourceId: int
        @param targetId: the identifier of target peer
        @type targetId: int
        @return: If connection was removed, returns True. Else, returns False.
        @rtype: bool
        """
        raise NotImplementedError()
    
    def getNeighbor(self, sourceId, targetId):
        """
        Gets a Neighbor.
        @param sourceId: the identifier of source node
        @type sourceId: int
        @param targetId: the identifier of target node
        @type targetId: int
        @return: an INeighbor
        @rtype: INeighbor
        """
        raise NotImplementedError()
    
    def getNeighbors(self, nodeId):
        """
        Gets the list of Neighbors in node
        @param nodeId: the identifier of node
        @type nodeId: int
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def countNeighbors(self, nodeId):
        """
        Counts the number of Neighbors in node
        @param nodeId: the identifier of node
        @type nodeId: int
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def setNetwork(self, peerToPeerNetwork):
        """
        Sets the peer-to-peer network.
        @param peerToPeerNetwork: an IPeerToPeerNetwork
        @type peerToPeerNetwork: IPeerToPeerNetwork
        @return: an IPeerToPeerNetwork
        @rtype: IPeerToPeerNetwork
        """
        raise NotImplementedError()
    
    def getNetwork(self):
        """
        Gets the peer-to-peer network.
        @return: an IPeerToPeerNetwork
        @rtype: IPeerToPeerNetwork
        """
        raise NotImplementedError()
    
    def addNode(self, nodeId):
        """
        Adds a node in topology.
        @param nodeId: the node identifier
        @type nodeId: int
        @return: If node was registered, returns True, else returns False.
        @rtype: bool
        """
        raise NotImplementedError()
    
    def removeNode(self, nodeId):
        """
        Adds a node in topology.
        @param nodeId: the node identifier
        @type nodeId: int
        @return: If node was removed, returns True, else returns False.
        @rtype: bool
        """
        raise NotImplementedError()
    
    def getPeer(self, PeerId):
        """
        Gets a Peer in topology.
        @param PeerId: the Peer identifier
        @type PeerId: int
        @return: a Peer
        @rtype: Peer
        """
        raise NotImplementedError()
    
    def getPeers(self):
        """
        Gets the list of Peer
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def countPeers(self):
        """
        Counts the number of Peers.
        @return: an int
        @rtype: int
        """
        raise NotImplementedError()
    
    def getNeighbors(self, peerId):
        """
        Gets the neighbors of peer
        @return: a list
        @rtype: list
        """
        raise NotImplementedError()
    
    def hasPeer(self, peerId):
        raise NotImplementedError()
    
   