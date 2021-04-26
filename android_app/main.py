from client import EchoClientFactory, reactor

from screens import StartScreen, QRreader, ConnectionScreen, MainScreen, CommandScreen

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition


class MainApp(App):
    connection = None
    textbox = None
    label = None

    def build(self):
        self.screenmanager = ScreenManager(transition=FadeTransition())
        self.screenmanager.add_widget(StartScreen(self, name='start'))
        self.screenmanager.add_widget(QRreader(self, name='QR'))
        self.screenmanager.add_widget(ConnectionScreen (self, name='connect'))
        self.screenmanager.add_widget(MainScreen(self, name='main'))
        self.screenmanager.add_widget(CommandScreen(self, name='command'))
        return self.screenmanager

    def connect_to_server(self, ip, port):
        reactor.connectTCP(ip, port, ClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
        connection.write("[DEV] device name, device ip")
        #sleep (1)
        self.screenmanager.current = 'main'

    def print_message(self, msg):
    	self.label.text = "{}\n".format(msg)


if __name__ == "__main__":
    app = MainApp()
    app.run()
