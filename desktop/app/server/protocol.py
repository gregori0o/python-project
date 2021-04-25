
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.python import failure
from typing import Tuple


class AppProtocol(Protocol):

    def __init__(self, factory: Factory):
        self.factory = factory
        
    
    def dataReceived(self, data: bytes):
        """ reaction for data received from client """
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)
            
    def connectionMade(self):
        self.factory.num_connections += 1
        
        
    def connectionLost(self, reason: failure.Failure):
        self.factory.num_connections -= 1