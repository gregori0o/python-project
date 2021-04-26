from twisted.internet.protocol import Protocol, Factory
from twisted.python.failure import Failure
from collections import namedtuple

class AppProtocol(Protocol):

    Client = namedtuple('Client', ('port', 'ip'))
    

    def __init__(self, factory: Factory):
        self.factory = factory
        
    
    def dataReceived(self, data: bytes):
        """ reaction for data received from client """
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)
            
    def connectionMade(self):
        self.factory.client = AppProtocol.Client(
            self.transport.getPeer().port,
            self.transport.getPeer().host
        )
        self.factory.ip = self.transport.getHost().host
        #debug
        print(f"Connection estabilished with {self.factory.client}") 

        
    def connectionLost(self, reason: Failure):
        print(f"Closed connection with {self.factory.client}")
        self.factory.client.port = None
        self.factory.client.host = None