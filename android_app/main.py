from __future__ import unicode_literals

from kivy.support import install_twisted_reactor

install_twisted_reactor()

# A Simple Client that send messages to the Echo Server
from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data.decode('utf-8'))


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        self.app.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        self.app.print_message('Lost connection.')

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Connection failed.')


from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy_garden.zbarcam import ZBarCam
from time import sleep


class MainApp(App):
    connection = None
    textbox = None
    label = ""

    def build(self):
        screenmanager = ScreenManager()
        screen_start = FirstStep(name='start')
        screen_QR = QRreader(self, name='QR')
        screen_main = MainScreen(self, name='main')
        screenmanager.add_widget(screen_start)
        screenmanager.add_widget(screen_QR)
        screenmanager.add_widget(screen_main)
        return screenmanager

    def connect_to_server(self, ip, port):
        reactor.connectTCP(ip, port, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def print_message(self, msg):
        pass
        #self.label += "{}\n".format(msg)
        #print(self.label)

       
class FirstStep (Screen):
    def __init__(self, **kwargs):
        super (FirstStep, self).__init__(**kwargs)

        first_layout = FloatLayout()
        label = Label(text="""
                        Hello from Kivy, this is remote control for computer app.\n
                        [u][b]To connect please press button.[/b][/u]""",
                      markup=True,
                      halign='center',
                      font_size='20sp',
                      size_hint=(.65, .2),
                      pos_hint={'x': .1, 'y': 0.8})
        first_layout.add_widget(label)
        to_connect = Button(text="To connect",
                      halign='center',
                      size_hint=(.5, .3),
                      pos_hint={'x': .25, 'y': .4})
        to_connect.bind(on_press = self.read_IP)
        first_layout.add_widget(to_connect)

        self.add_widget(first_layout)

    def read_IP(self, *args):
        self.manager.current = 'QR'


class QRreader (Screen):
    def __init__(self, app, **kwargs):
        super (QRreader, self).__init__(**kwargs)
        self.app = app

        QR_layout = FloatLayout()
        label = Label(text="Take photo of QR code or enter data",
                      halign='center',
                      font_size='20sp',
                      size_hint=(.6, .1),
                      pos_hint={'x': .2, 'y': 0.9})
        QR_layout.add_widget(label)
        self.zbarcam = ZBarCam (
                      size_hint=(.6, .4),
                      pos_hint={'x': .2, 'y': 0.5})
        QR_layout.add_widget(self.zbarcam)
        self.read_text = TextInput(
                      text = ', '.join([str(symbol.data) for symbol in self.zbarcam.symbols]),
                      multiline=False,
                      readonly=False,
                      halign="left",
                      font_size=30,
                      size_hint=(.8, .1),
                      pos_hint={'x': .1, 'y': 0.4})
        QR_layout.add_widget(self.read_text)
        make_photo = Button(text="Make photo",
                      halign='center',
                      size_hint=(.5, .1),
                      pos_hint={'x': .25, 'y': .25})
        make_photo.bind(on_press = self.make_photo)
        QR_layout.add_widget(make_photo)
        confirm = Button(text="Confirm",
                      halign='center',
                      size_hint=(.5, .1),
                      pos_hint={'x': .25, 'y': .1})
        confirm.bind(on_press = self.confirm)
        QR_layout.add_widget(confirm)

        self.add_widget(QR_layout)

    def confirm (self, *args):
        data = self.read_text.text

        ip = data.split(',')[0]
        port = data.split(',')[1]
        #ip = "192.168.100.89"
        #port = 8000  
        
        self.app.connect_to_server(ip, port)
        self.manager.current = 'main'
        #if not self.app.connection:
        #    self.read_text.text = "Connection failed. Enter new data."
        #else:
        #    #self.zbarcam.stop()
        #    self.manager.current = 'main'

    def make_photo (self, *args):
        self.read_text.text = ', '.join([str(symbol.data) for symbol in self.zbarcam.symbols])


class MainScreen (Screen):
    def __init__(self, app, **kwargs):
        super (MainScreen, self).__init__(**kwargs)
        self.app = app

        main_layout = FloatLayout()
        label = Label(text="Enter command for computer.",
                      halign='center',
                      font_size='20sp',
                      size_hint=(.6, .1),
                      pos_hint={'x': .2, 'y': 0.9})
        main_layout.add_widget(label)
        self.read_text = TextInput(
                      multiline=True,
                      readonly=False,
                      halign="left",
                      font_size=30,
                      size_hint=(.8, .3),
                      pos_hint={'x': .1, 'y': 0.5})
        main_layout.add_widget(self.read_text)
        execute = Button(text="Execute command",
                      halign='center',
                      size_hint=(.5, .1),
                      pos_hint={'x': .25, 'y': .25})
        execute.bind(on_press = self.execute)
        main_layout.add_widget(execute)

        self.add_widget(main_layout)

    def execute (self, *args):
        msg = self.read_text.text

       
        if msg and self.app.connection:
            self.app.connection.write(msg.encode('utf-8'))
            self.read_text.text = "Nice"
        else:
            self.read_text.text = "Some problem"

if __name__ == "__main__":
    app = MainApp()
    app.run()