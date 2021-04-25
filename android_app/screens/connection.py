from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class ConnectionScreen (Screen):
    def __init__(self, app, **kwargs):
        super (ConnectionScreen, self).__init__(**kwargs)
        self.app = app

        connection_layout = FloatLayout()
        label_info = Label(text="Connect...",
                      halign='center',
                      font_size='20sp',
                      size_hint=(.65, .2),
                      pos_hint={'x': .1, 'y': 0.8})
        connection_layout.add_widget(label_info)
        self.app.label = Label(halign='center',
        			  font_size='20sp',
        			  size_hint=(.65, .2),
                      pos_hint={'x': .1, 'y': 0.55})
        connection_layout.add_widget(self.app.label)
        
        self.add_widget(connection_layout)