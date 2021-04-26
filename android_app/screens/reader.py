from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy_garden.zbarcam import ZBarCam


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
                      text = "Make photo",
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
        try:
        	ip = data.split(',')[0]
        	port = data.split(',')[1]
        except:
        	return
        f = open ("remote_app_data.txt", "w")
        f.write (data)
        f.close ()
        self.app.connect_to_server(ip, int(port))
        self.manager.current = 'connect'

    def make_photo (self, *args):
    	text = ', '.join([str(symbol.data) for symbol in self.zbarcam.symbols])
    	if "'" in text:
    		text = text.split("'")[1]
    	self.read_text.text = text