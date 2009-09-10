from pydssim.network.route.abstract_route import AbstractRoute

class ContentRoute(AbstractRoute):
    
    def __init__(self, elementId, trace):
        self.initialize(0, elementId, trace)