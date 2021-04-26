from __future__ import unicode_literals
from typing import Literal                     # Kivy needs this 
from collections.abc import Callable
from collections import namedtuple

from kivy.support import install_twisted_reactor

# documentations says that install_twisted_reactor must be called 
# before importing reactor from twisted.internet
install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory, Protocol
from server.protocol import AppProtocol
import os


class Server(Factory):

    DEFAULT_PORT: Literal = 8000

    
    def __init__(self, app):
        self.app = app
        self.client = None
        
        # spliting in case device is connected on more than one interface
        self.ip = os.popen('hostname -I').read().split(' ')[0]
        self.port = Server.DEFAULT_PORT
        
        
    # def startFactory(self):
    #     pass


    # def stopFactory(self):
    #     pass


    def buildProtocol(self, addr: tuple[str, int]) -> "Protocol":
            return AppProtocol(self)

    
    def run(self):
        endpoint = TCP4ServerEndpoint(reactor, Server.DEFAULT_PORT, interface='')
        endpoint.listen(self)
        # reactor.run()
    