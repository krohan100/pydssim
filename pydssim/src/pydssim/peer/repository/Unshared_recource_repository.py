from pydssim.peer.repository.abstract_repository import AbstractRepository

class UnSharedRecourceRepository(AbstractRepository):
    
    def __init__(self, peer):
        self.initialize(peer)