from twisted.internet.protocol import Protocol, Factory
from server.protocol import AppProtocol
from typing import Tuple
from main import DesktopApp

            
class AppProtocolFactory(Factory):

    def __init__(self, 
                 app: DesktopApp,
                 callback_port_occupied):
        self.app = app
        self.num_connections = 0

        
    def buildProtocol(self, addr: tuple[str, int]) -> "Protocol":
        if self.num_connections == 0:
            return AppProtocol(self)
        else:
            print("Port already occupied")