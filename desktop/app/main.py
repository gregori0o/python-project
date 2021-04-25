""" Desktop application """
import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
import os
import qrcode

from server.server import Server

DEFAULT_PORT = 8000

class QRCodeButton(Button):
    state = BooleanProperty(True)
    def __init__(self, **kwargs):
        super(QRCodeButton, self).__init__(**kwargs)
        self.text = 'Click me to get the QR code'
        
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('Generating QR Code...') 
            self.state = not self.state
            
            return True
        return super().on_touch_down(touch)

        


class DesktopApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # spliting in case device is connected by more than one interface
        # self.ipv4_server_address = os.popen('hostname -I').read().split(' ')[0]
        self.server = Server(self, )
        self.server.listen()
    
    
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.screens = {'main': Screen(name='main'), 'qrcode': Screen(name='qrcode')}
        self.screen_manager.add_widget(self.screens['main'])
        self.screen_manager.add_widget(self.screens['qrcode'])

        
        self.main_layout = BoxLayout()
        self.qrcode_button = QRCodeButton()
        self.qrcode_button.bind(state=self.show_qrcode)
        self.main_layout.add_widget(self.qrcode_button)
 
        self.screens['main'].add_widget(self.main_layout)

        self.qrcode_layout = BoxLayout()
        # self.qrcode_layout.add_widget(Image(source='qrcode.png'))
        self.screens['qrcode'].add_widget(self.qrcode_layout) 
        
        return self.screen_manager
        

    def handle_message(self, data: bytes):
        print(data.decode('utf-8'))

    
    def show_qrcode(self, instance, pos):
        if len(self.qrcode_layout.children) == 0:
            qrcode_img = qrcode.make(f"{self.ipv4_server_address},{DEFAULT_PORT}")
            qrcode_img.save('qrcode/qrcode.png', format='png')
            self.qrcode_layout.add_widget(Image(source='qrcode/qrcode.png'))
        self.screen_manager.switch_to(self.screens['qrcode'])
    
    

    
def main():
    DesktopApp().run()

if __name__ == '__main__':
    main()