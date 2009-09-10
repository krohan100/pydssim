from pydssim.network.message.abstract_message import AbstractMessage

class DefaultMessage(AbstractMessage):
    
    def __init__(self, id, sourceId, targetId, ttl, priority):
        self.initialize("DEFAULT",  sourceId, targetId, ttl, priority)