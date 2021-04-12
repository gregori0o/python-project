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

from server.twistedserver import *

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

    def on_state(self, instance, pos):
        pass

        


class Application(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.screens = [Screen(name='main'), Screen(name='qrcode')]
        self.screen_manager.add_widget(self.screens[0])
        self.screen_manager.add_widget(self.screens[1])

        
        self.main_layout = BoxLayout()
        self.qrcode_button = QRCodeButton()
        self.qrcode_button.bind(state=self.show_qrcode)
        self.main_layout.add_widget(self.qrcode_button)
 
        self.screens[0].add_widget(self.main_layout)

        self.qrcode_layout = BoxLayout()
        # self.qrcode_layout.add_widget(Image(source='qrcode.png'))
        self.screens[1].add_widget(self.qrcode_layout) 
        
        reactor.listenTCP(DEFAULT_PORT, ServerFactory(self))
        
        self.ipv4_server_address = os.popen('hostname -I').read()

        
        return self.screen_manager
    

    def handle_message(self, data: bytes):
        print(data.decode('utf-8'))
        
    
    def show_qrcode(self, instance, pos):
        if len(self.qrcode_layout.children) == 0:
            qrcode_img = qrcode.make(f"{self.ipv4_server_address},{DEFAULT_PORT}")
            qrcode_img.save('qrcode.png', format='png')
            self.qrcode_layout.add_widget(Image(source='qrcode.png'))
        self.screen_manager.switch_to(self.screens[1])

    
    
    
    
def main():
    Application().run()


    
if __name__ == '__main__':
    main()
    