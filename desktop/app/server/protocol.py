from twisted.internet.protocol import Protocol, Factory
from twisted.python.failure import Failure
from collections import namedtuple


Client = namedtuple('Client', ('port', 'ip'))

class AppProtocol(Protocol):

    def __init__(self, factory: Factory):
        self.factory = factory
        
    
    def dataReceived(self, data: bytes):
        """ reaction for data received from client """
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)
            
    def connectionMade(self):
        self.factory.client = Client(
            self.transport.getPeer().port,
            self.transport.getPeer().host)
        self.factory.ip = self.transport.getHost().host
        self.factory.connection = self
        print(f"Connection estabilished with {self.factory.client}") 
        self.factory.on_connection_made(self.factory.info)

        
    def connectionLost(self, reason: Failure):
        print(f"Closed connection with {self.factory.client}")
        self.factory.client = None
        self.factory.connection = None
