from __future__ import unicode_literals
from kivy.support import install_twisted_reactor

# documentations says that install_twisted_reactor must be called 
# before importing reactor from twisted.internet
install_twisted_reactor()

from twisted.internet import reactor, protocol


class Server(protocol.Protocol):
    def dataReceived(self, data: bytes):
        """ reaction for data received from client """
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)
            
            
class ServerFactory(protocol.Factory):
    protocol = Server

    def __init__(self, app):
        self.app = app

