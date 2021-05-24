from typing import Literal                     # Kivy needs this 
from kivy.support import install_twisted_reactor

# documentation says that install_twisted_reactor must be called 
# before importing reactor from twisted.internet
install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.protocol import Factory, Protocol
from server.protocol import AppProtocol
from collections import namedtuple
import socket
import os




ServerInfo = namedtuple('ServerInfo', 'ip port')

# class ServerInfo(object):
#     def __init__(self, ip: str, port: int):
#         self.ip = ip
#         self.port = port
#         self._lock = True

#     @property
#     def ip(self):
#         return self._ip
    
#     @ip.setter
#     def ip(self, value: str):
#         if not self._lock:
#             self._ip = value
        
#     @property
#     def port(self):
#         return self._port
    
#     @port.setter
#     def port(self, value: int):
#         if not self._lock:
#             self._port = value



class Server(Factory):

    DEFAULT_PORT: Literal[4000] = 4000


    def __init__(self, app):
        self.app = app
        self.client = None
        
        # spliting in case device is connected on more than one interface
        # this code is OS specific
        self._ip = os.popen('hostname -I').read().split(' ')[0]

        # may throw IOError exception
        self._port = self._find_free_port(Server.DEFAULT_PORT)
        
    def _find_free_port(self, port: int = 4000, max_port: int = 60_000):
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
        endpoint = TCP4ServerEndpoint(reactor, self._port, interface='')
        endpoint.listen(self)
        # reactor.run()
    
    @property
    def info(self):
        return ServerInfo(ip=self._ip, port=self._port)
        
    
    
        