from __future__ import unicode_literals
from typing import Literal                     # Kivy needs this 
from collections.abc import Callable


from kivy.support import install_twisted_reactor

# documentations says that install_twisted_reactor must be called 
# before importing reactor from twisted.internet
install_twisted_reactor()
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from server.protocolfactory import AppProtocolFactory
from main import DesktopApp



class Server(object):

    DEFAULT_PORT: Literal = 8000
    
    
    def __init__(self, app: DesktopApp, received_data_handler: Callable):
        self.app = app
        self.data_handler = received_data_handler
        self.protocol_factor = AppProtocolFactory(app, self.data_handler)
    
    
    def listen(self):
        endpoint = TCP4ServerEndpoint(reactor, Server.DEFAULT_PORT, interface='')
        endpoint.listen(AppProtocolFactory(self.app, self.data_handler))
        reactor.run()
        