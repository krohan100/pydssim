from pydssim.network.dispatcher.abstract_message_handler import AbstractMessageHandler
from pydssim.util.decorator.public import public
#from pysocialsim.p2p.profile.default_interest_matching_strategy import DefaultInterestMatchingStrategy
from pydssim.network.advertisement.content_advertisement import ContentAdvertisement
re from pysocialsim.p2p.routing.content_route import ContentRoute

class AdvertiseContentMessageHandler(AbstractMessageHandler):
    
    def __init__(self, peer):
        self.initialize("ADVERTISE_CONTENT", peer)
    
    @public
    def clone(self):
        return AdvertiseContentMessageHandler(self.getPeer())
    
    def executeHandler(self):
        message = self.getMessage()
        if message.getHop() < message.getTTL():
            peer = self.getPeer()
            
            advertisement = ContentAdvertisement(message.getTraces()[0], message.getParameter("contentId"), message.getParameter("resources"), message.getParameter("type"))
            
            #profile = peer.getProfile()
            #profile.matchInterests(advertisement, DefaultInterestMatchingStrategy())
            
            neighbor = peer.getNeighbor(message.getSourceId())
            neighbor.addRoute(ContentRoute(advertisement.getElementId(), message.getTraces()))
            
            neighbors = peer.getNeighbors()
            
            for n in neighbors:
                if n.getId() in message.getTraces():
                    continue
                
                msg = message.clone()
                msg.registerTrace(peer.getId())
                msg.setHop(msg.getHop() + 1)
                msg.setTargetId(n.getId())
                msg.setSourceId(peer.getId())
                peer.send(msg)
            