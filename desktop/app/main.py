""" Desktop application """
import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from server.twistedserver import *


class Application(App):
    def build(self):
        self.layout = BoxLayout()
        self.qrcode_button = Button(text='Click to get QR Code')
        
        self.layout.add_widget(self.qrcode_button)
 
        reactor.listenTCP()
        
        
        return self.layout
    
    
def main():
    Application().run()


    
if __name__ == '__main__':
    main()
    