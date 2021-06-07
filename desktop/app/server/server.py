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


from abc import ABC, abstractmethod
class ConnectionObserver(ABC):
    
    @abstractmethod
    def on_connection_made(self, server_info: ServerInfo) -> None:
        raise NotImplementedError


    @abstractmethod
    def on_connection_lost(self, server_info: ServerInfo) -> None:
        raise NotImplementedError



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
        self.connection = None
        # spliting in case device is connected on more than one interface
        # this code is OS specific
        if os.name == 'posix':
            self.__ip = os.popen('hostname -I').read().split(' ')[0]
        else:
            tmp = socket.gethostname()
            self.__ip = socket.gethostbyname(tmp).split()[0]
        self.__port = self.__find_free_port(Server.DEFAULT_PORT)
        self.__connection_observers: list[ConnectionObserver] = []

        
    def __find_free_port(self, port: int = 4000, max_port: int = 60_000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while port <= max_port:
            try:
                sock.bind(('', port))
                sock.close()
                return port
            except OSError:
                port += 1
        raise OSError('No free port available')
    

    def buildProtocol(self, addr: tuple[str, int]) -> "Protocol":
        print('Server.buildProtocol:', addr)
        return AppProtocol(self)
            

    def run(self):
        endpoint = TCP4ServerEndpoint(reactor, self.__port, interface='')
        endpoint.listen(self)
        # reactor.run()

        
    def closeConnection(self):
        if self.connection is not None:
            print('Server.closeConnection')
            self.connection.transport.loseConnection()
            self.connection = None
            for observer in self.__connection_observers:
                observer.on_connection_lost(self.info)
        
    
    @property
    def info(self):
        return ServerInfo(ip=self.__ip, port=self.__port)
        

    def add_observer(self, observer: ConnectionObserver):
        self.__connection_observers.append(observer)
        
    
    def on_connection_made(self, server_info: ServerInfo) -> None:
        for observer in self.__connection_observers:
            observer.on_connection_made(server_info)