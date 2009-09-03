from pydssim.network.topology.abstract_topology import AbstractTopology
from pydssim.util.decorator.public import public



class DefaultTopology(AbstractTopology):
    
    def __init__(self):
        self.initialize()
        
    @public
    def connect(self, peer):
        pass
        
    @public
    def disconnect(self, peer):
        raise NotImplementedError()