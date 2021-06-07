from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
import server
from server.server import ServerInfo, ConnectionObserver
from ui.buttons import QRCodeButton
import abc

class MainScreen(Screen):

    def __init__(self, name: str, server_info: ServerInfo, **kwargs):
        super().__init__(name=name, **kwargs)
        # print(self.manager)
        self.qrcode_button = QRCodeButton()
        self.qrcode_button.size_hint = (.3, .2)
        self.qrcode_button.pos_hint = {'x': .7, 'y': .8}
        # self.layout = BoxLayout(orientation='horizontal')
        self.layout = FloatLayout()
        # self.qrcode_button.bind(state=self.show_qrcode)

        self.status_label = Label(text='No device connected\nip: -\nport: -',
                                  font_size=20,
                                  pos_hint={'center_x': .85, 'center_y': .7})
        self.status_label.color = [1.0, 0, 0, 1]
        
        self.command_output_header = Label(text='===== COMMAND OUTPUT =====',
                                    font_size=20,
                                    pos_hint={'center_x': .4, 'center_y': .95})
        self.command_output = Label(text='Command:',
                                    font_size=20,
                                    pos_hint={'x': -.4, 'y': 0.9})
        
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(self.qrcode_button)
        self.layout.add_widget(self.command_output_header)
        self.layout.add_widget(self.command_output)
        self.add_widget(self.layout)
        

    def on_connection_made(self, server_info: ServerInfo) -> None:
        self.status_label.text = f'Device connected\nip: {server_info.ip}\nport: {server_info.port}'
        self.status_label.color = [0, 1.0, 0, 1]

        
    def on_connection_lost(self, server_info: ServerInfo) -> None:
        self.status_label.text = f'Device disconnected\nip: -\nport: -'
        self.status_label.color = [1.0, 0, 0, 1]

        
    def on_command_output(self, command: str, output: str) -> None:
        if command is not None or output is not None:
            self.command_output.text = 'Command: ' + command + '\nOutput:\n' + output
            self.command_output.pos_hint = {'x': 0, 'y': 0.1}

        
            

class BackMainButtonObserver(abc.ABC):

    @abc.abstractmethod
    def on_back_main_pressed():
        raise NotImplementedError


class QRCodeScreen(Screen):
    
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        
        self.__qrcode = None
        self.layout = BoxLayout()
        self.back_main_button = Button(text="Back to main screen",
                                       size_hint=(1, .2))
        self.back_main_button.on_press = self.on_back_main_pressed
        self.layout.add_widget(self.back_main_button)
        self.add_widget(self.layout)
        
        self.observers: list[BackMainButtonObserver] = []
       
       
    def on_back_main_pressed(self):
        for observer in self.observers:
            observer.on_back_main_pressed()
        

    def add_back_main_button_observer(self, observer: BackMainButtonObserver):
        if observer not in self.observers:
            self.observers.append(observer)


    @property
    def qrcode(self):
        return self._qrcode
    
    
    @qrcode.setter
    def qrcode(self, img: Image):
        if self.__qrcode is None:
            self.__qrcode = img
            self.add_widget(img)