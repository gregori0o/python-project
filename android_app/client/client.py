from __future__ import unicode_literals

from kivy.support import install_twisted_reactor

install_twisted_reactor()

# A Simple Client that send messages to the Echo Server
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor


class ClientProtocol(Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data.decode('utf-8'))


class ClientFactory(Factory):
    protocol = ClientProtocol

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        self.app.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        self.app.print_message('Lost connection.')
        self.app.screenmanager.current = 'start'

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Connection failed.')
        #sleep(1)
        self.app.screenmanager.current = 'QR'
