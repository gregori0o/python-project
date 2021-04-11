import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

kivy.require('2.0.0')

class QRCodeButton(Button):
    def __init__(self, **kwargs):
        super(QRCodeButton, self).__init__(**kwargs)
        
        self.text = 'Click me to get the QR code'
        
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('Generating QR Code...') 
            return True
        return super().on_touch_down(touch)

        
    def generate_qrcode(self):
        pass
        


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        
        qrcode_button = QRCodeButton()
        
        self.add_widget(qrcode_button)
        
    
    # def on_qrcode_button(self):
        
        
class Application(App):
    def build(self):
        return MainWindow()
    
    def start(self):
        print('Starting application...')
        self.run()
        


if __name__ == '__main__':
    Application().run()
