from kivy.uix.button import Button
from kivy.uix.image import Image
import abc



class QRCodeButtonObserver(abc.ABC):

    @abc.abstractmethod
    def on_qr_button_pressed(self):
        raise NotImplementedError('on_pressed')
    

class QRCodeButton(Button):
    
    def __init__(self, **kwargs):
        super(QRCodeButton, self).__init__(**kwargs)
        self.text = 'Click me to get the QR code'
        self._observers: list[QRCodeButtonObserver] = []
        
        
    def add_observer(self, observer: QRCodeButtonObserver):
        if observer not in self._observers:
            self._observers.append(observer)
        

    def on_touch_down(self, touch):
        # print('qrcode button pressed')
        if self.collide_point(*touch.pos):
            # print("QRCodeButton pressed at", touch.pos, 'Notifing observers')
            for observer in self._observers:
                observer.on_qr_button_pressed()
            return True
        return super().on_touch_down(touch)