from pysocialsim.p2p.routing.abstract_neighbor import AbstractNeighbor

class DefaultNeighbor(AbstractNeighbor):
    
    def __init__(self, peer, id):
        self.initialize(peer, id)