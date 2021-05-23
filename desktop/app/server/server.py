from __future__ import unicode_literals
from typing import Literal                     # Kivy needs this 
from collections.abc import Callable
from collections import namedtuple

from kivy.support import install_twisted_reactor

# documentation says that install_twisted_reactor must be called 
# before importing reactor from twisted.internet
install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory, Protocol
from server.protocol import AppProtocol
import socket
import os


class Server(Factory):

    DEFAULT_PORT: Literal[4000] = 4000


    def __init__(self, app):
        self.app = app
        self.client = None
        
        # spliting in case device is connected on more than one interface
        # this code is OS specific
        self.ip = os.popen('hostname -I').read().split(' ')[0]

        # may throw IOError exception
        self.port = self.find_free_port(Server.DEFAULT_PORT)


    def find_free_port(self, port: int = 4000, max_port: int = 60_000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind(('', port))
                sock.close()
                return port
            except OSError:
                port += 1
        raise IOError('No free port available')
    

    def buildProtocol(self, addr: tuple[str, int]) -> "Protocol":
            print('Server.buildProtocol:', addr)
            return AppProtocol(self)
            
    
    def run(self):
        endpoint = TCP4ServerEndpoint(reactor, self.port, interface='')
        endpoint.listen(self)
        # reactor.run()
    