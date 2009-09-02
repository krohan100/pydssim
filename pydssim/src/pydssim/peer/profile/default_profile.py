from pydssim.peer.profile.abstract_profile import AbstractProfile

class DefaultProfile(AbstractProfile):
    
    def __init__(self, peer):
        self.initialize(peer)