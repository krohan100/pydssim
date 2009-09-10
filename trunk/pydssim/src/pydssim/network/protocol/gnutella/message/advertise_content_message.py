from pydssim.network.message.abstract_message import AbstractMessage
from pydssim.util.decorator.public import public

class AdvertiseContentMessage(AbstractMessage):
    
    def __init__(self, id, sourceId, targetId, ttl, priority):
        self.initialize("ADVERTISE_CONTENT", id, sourceId, targetId, ttl, priority)
    
    @public
    def clone(self):
        message = AdvertiseContentMessage(self.getId(), self.getSourceId(), self.getTargetId(), self.getTTL(), self.getPriority())
        message.setHop(self.getHop())
        for id in self.getTraces():
            message.registerTrace(id)
        for name in self.getParameterNames():
            message.setParameter(name, self.getParameter(name))
        return message