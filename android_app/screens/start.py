from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class StartScreen (Screen):
    def __init__(self, app, **kwargs):
        super (StartScreen, self).__init__(**kwargs)

        self.app = app

        first_layout = FloatLayout()
        exit_button = Button(text="Exit",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .9})
        exit_button.bind(on_press = self.app.stop)
        first_layout.add_widget(exit_button)
        label_info = Label(text="""
                        Remote control for computer.\n
                        To connect with latest data -> 'Restart'.\n
                        To connect with new data -> 'Connect'.""",
                      markup=True,
                      halign='left',
                      font_size='20sp',
                      size_hint=(1, .35),
                      pos_hint={'x': .0, 'y': 0.53})
        first_layout.add_widget(label_info)
        to_connect = Button(text="Connect",
                      halign='center',
                      size_hint=(.3, .3),
                      pos_hint={'x': .1, 'y': .2})
        to_connect.bind(on_press = self.QR_reader)
        first_layout.add_widget(to_connect)
        latest_connection = Button(text="Restart",
                      halign='center',
                      size_hint=(.3, .3),
                      pos_hint={'x': .6, 'y': .2})
        latest_connection.bind(on_press = self.connect_with_data)
        first_layout.add_widget(latest_connection)

        self.add_widget(first_layout)

    def QR_reader(self, *args):
    	self.manager.current = 'QR'

    def connect_with_data (self, *args):
    	try:
    		f = open ("remote_app_data.txt", "r")
    		data = f.read()
    		f.close()
    		ip = data.split(',')[0]
    		port = int(data.split(',')[1])
    	except:
    		ip = "192.168.100.89"
    		port = 8000
    	finally:
    		self.app.connect_to_server(ip, port)
    		self.manager.current = 'connect'
