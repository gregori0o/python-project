from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from server.server import ServerInfo
from ui.buttons import QRCodeButton
import abc


class MainScreen(Screen):
    def __init__(self, name: str, server_info: ServerInfo, **kwargs):
        super().__init__(name=name, **kwargs)
        print(self.manager)
        self.layout = BoxLayout(orientation='horizontal')

        self.qrcode_button = QRCodeButton()
        # self.qrcode_button.bind(state=self.show_qrcode)

        self.layout.add_widget(self.qrcode_button)
        self.add_widget(self.layout)


class BackMainButtonObserver(abc.ABC):
    @abc.abstractmethod
    def on_back_main_pressed():
        raise NotImplementedError


class QRCodeScreen(Screen):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        
        self._qrcode = None
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
        if self._qrcode is None:
            self._qrcode = img
            self.add_widget(img)
        
       
       
