""" Desktop application """
import os
import kivy

kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
import qrcode

from server.server import Server, ServerInfo
from parser.cmdparser import CommandHandler, CommandHandlerObserver

from ui.buttons import QRCodeButtonObserver
from ui.screens import MainScreen, QRCodeScreen


class DesktopApp(App, QRCodeButtonObserver, CommandHandlerObserver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        current_dir = os.scandir('./')
        for entry in current_dir:
            if entry.name == 'qrcode' and entry.is_dir():
                break
        else:
            os.mkdir('./qrcode', 0o777)
                
        
        try: 
            self.server = Server(self)
        except OSError as err:
            print("Failed to create Server instance,", err.strerror)
            exit(err.errno)

        # self.qrcode_generated = False
        self.command_handler = CommandHandler()
        self.command_handler.add_observer(self)
        self.server_info = self.server.info
        self.server.run()
        
        
    def build(self):
        self.screen_manager = ScreenManager()

        self.main_screen = MainScreen('main', self.server_info)
        self.main_screen.qrcode_button.add_observer(self)
        
        self.qrcode_screen = QRCodeScreen('qrcode')
        self.qrcode_screen.add_back_main_button_observer(self)
        
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.qrcode_screen)
        
        return self.screen_manager


    def handle_message(self, data: bytes):
        try:
            self.command_handler(data.decode('utf-8'))
        except ValueError as err:
            print('ValueError')
        except TypeError as err:
            print('TypeError')


    def show_qrcode(self, *args):
        qrcode_img = qrcode.make(f"{self.server_info.ip},{self.server_info.port}")
        qrcode_img.save('qrcode/qrcode.png', format='png')
        # if not self.qrcode_generated:
            # self.add_widget(Image(source='qrcode/qrcode.png'))
            # self.qrcode_generated = True
        self.qrcode_screen.qrcode = Image(source='qrcode/qrcode.png')
        self.screen_manager.current = 'qrcode'
    
    
    def on_qr_button_pressed(self):
        self.show_qrcode()
        

    def on_back_main_pressed(self):
        self.screen_manager.current = 'main'
        
        
    def on_disconnect(self):
        self.server.closeConnection()
        
        
    
def main():
    DesktopApp().run()


if __name__ == '__main__':
    main()