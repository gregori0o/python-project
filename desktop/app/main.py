""" Desktop application """
from os.path import supports_unicode_filenames
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
        self.server = Server(self)
        self.server.run()
        self.qrcode_generated = False
    
    
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.screens = {'main': Screen(name='main'), 'qrcode': Screen(name='qrcode')}
        self.screen_manager.add_widget(self.screens['main'])
        self.screen_manager.add_widget(self.screens['qrcode'])
        
        self.main_screen_layout = BoxLayout()
        self.qrcode_button = QRCodeButton()
        self.qrcode_button.bind(state=self.show_qrcode)
        self.main_screen_layout.add_widget(self.qrcode_button)
 
        self.qrcode_screen_layout = BoxLayout()
        self.back_main_button  = Button(text="Back to main screen",
                                        size_hint=(0.3, 1))
        self.back_main_button.bind(on_press=self.goto_main_screen)
        # self.back_main_button.on_touch_down = self.goto_main_screen
        self.qrcode_screen_layout.add_widget(self.back_main_button)
        
        self.screens['main'].add_widget(self.main_screen_layout)
        self.screens['qrcode'].add_widget(self.qrcode_screen_layout) 
        
        return self.screen_manager


    def handle_message(self, data: bytes):
        print(data.decode('utf-8'))
        

    
    def show_qrcode(self, *args):
        qrcode_img = qrcode.make(f"{self.server.ip},{self.server.port}")
        qrcode_img.save('qrcode/qrcode.png', format='png')
        if not self.qrcode_generated:
            self.qrcode_screen_layout.add_widget(Image(source='qrcode/qrcode.png'))
            self.qrcode_generated = True
        # else: 
            # self.qrcode_screen_layout.children[0] = Image(source='qrcode/qrcode.png')
        self.screen_manager.current = 'qrcode'
    
    # def show_mainscreen(self, instance, pos)
    def goto_main_screen(self, instance):
        print("swapping to main screen")
        self.screen_manager.current = 'main'
    

class MainScreen(Screen):
    
    def __init__(self, name: str, qrcode_generator, *args, **kwargs):
        super.__init__(name=name, **kwargs)
        self.layout = BoxLayout(orientation='horizontal')
        
        self.qrcode_button = QRCodeButton()   

        self.qrcode_button.bind(on_press=qrcode_generator(*args))

        
        self.add_widget(self.layout)
        
        


    
def main():
    DesktopApp().run()


if __name__ == '__main__':
    main()