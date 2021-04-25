from client import EchoClientFactory, reactor

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy_garden.zbarcam import ZBarCam
from kivy.graphics import Color, Rectangle

from time import sleep


class MainApp(App):
    connection = None
    textbox = None
    label = None

    def build(self):
        self.screenmanager = ScreenManager(transition=FadeTransition())
        self.screenmanager.add_widget(StartScreen(self, name='start'))
        self.screenmanager.add_widget(QRreader(self, name='QR'))
        self.screenmanager.add_widget(ConnectionScreen (self, name='connect'))
        self.screenmanager.add_widget(MainScreen(self, name='main'))
        self.screenmanager.add_widget(CommandScreen(self, name='command'))
        return self.screenmanager

    def connect_to_server(self, ip, port):
    	reactor.connectTCP(ip, port, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
        #sleep (1)
        self.screenmanager.current = 'main'

    def print_message(self, msg):
    	self.label.text = "{}\n".format(msg)
    	print (self.label.text)


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
                        Hello from Kivy, this is remote control for computer app.\n
                        To connect with latest data please press button 'Restart'.\n
                        To connect with new data please press button 'Connect'.""",
                      markup=True,
                      halign='center',
                      font_size='20sp',
                      size_hint=(.65, .2),
                      pos_hint={'x': .1, 'y': 0.6})
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
    	

class TouchPad (FloatLayout):
	def __init__ (self, app, **kwargs):
		super (TouchPad, self).__init__(**kwargs)
		with self.canvas.before:
			Color(0.22, 0.24, .26, mode='rgb')
			self.rect = Rectangle(size=self.size, pos=self.pos)
		self.bind(size=self._update_rect, pos=self._update_rect)
		self.app = app
		self.color = 'blue'
		left = Button(size_hint=(.5, .1),
		              pos_hint={'x': .0, 'y': .0})
		left.bind(on_press = self.left)
		self.add_widget(left)
		right = Button(size_hint=(.5, .1),
	                  pos_hint={'x': .5, 'y': .0})
		right.bind(on_press = self.right)
		self.add_widget(right)
		

	def _update_rect(self, instance, value):
		self.rect.pos = instance.pos
		self.rect.size = instance.size

	def left (self, *args):
		pass

	def right (self, *args):
		pass



class MainScreen (Screen):
    def __init__(self, app, **kwargs):
        super (MainScreen, self).__init__(**kwargs)
        self.app = app

        main_layout = FloatLayout()
        exit = Button(text="Exit",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .9})
        exit.bind(on_press = self.exit)
        main_layout.add_widget(exit)
        command = Button(text="Enter command",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .9})
        command.bind(on_press = self.command)
        main_layout.add_widget(command)

        button_l1 = Button(text="button_l1",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .79})
        #button_l1.bind(on_press = self.button_l1)
        main_layout.add_widget(button_l1)
        button_r1 = Button(text="button_r1",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .79})
        #button_r1.bind(on_press = self.button_r1)
        main_layout.add_widget(button_r1)
        button_l2 = Button(text="button_l2",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .68})
        #button_l2.bind(on_press = self.button_l2)
        main_layout.add_widget(button_l2)
        button_r2 = Button(text="button_r2",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .68})
        #button_r2.bind(on_press = self.button_r2)
        main_layout.add_widget(button_r2)
        button_l3 = Button(text="button_l3",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .57})
        #button_l3.bind(on_press = self.button_l3)
        main_layout.add_widget(button_l3)
        button_r3 = Button(text="button_r3",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .57})
        #button_r3.bind(on_press = self.button_r3)
        main_layout.add_widget(button_r3)
        button_l4 = Button(text="button_l4",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .46})
        #button_l4.bind(on_press = self.button_l4)
        main_layout.add_widget(button_l4)
        button_r4 = Button(text="button_r4",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .46})
        #button_r4.bind(on_press = self.button_r4)
        main_layout.add_widget(button_r4)
        mouse = TouchPad (app, size_hint=(1, .4),
                      pos_hint={'x': .0, 'y': .0})
        main_layout.add_widget(mouse)

        self.add_widget(main_layout)

    def exit (self, *args):
    	self.manager.current = 'start'

    def command (self, *args):
    	self.manager.current = 'command'





class CommandScreen (Screen):
    def __init__(self, app, **kwargs):
        super (CommandScreen, self).__init__(**kwargs)
        self.app = app

        command_layout = FloatLayout()
        back = Button(text="<---",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .9})
        back.bind(on_press = self.back)
        command_layout.add_widget(back)
        self.label = Label(text = "\nEnter command",
        			  halign='center',
                      font_size='20sp',
                      size_hint=(.6, .1),
                      pos_hint={'x': .2, 'y': 0.9})
        command_layout.add_widget(self.label)
        self.read_text = TextInput(
                      multiline=True,
                      readonly=False,
                      halign="left",
                      font_size=30,
                      size_hint=(.8, .3),
                      pos_hint={'x': .1, 'y': 0.5})
        command_layout.add_widget(self.read_text)
        execute = Button(text="Execute command",
                      halign='center',
                      size_hint=(.5, .1),
                      pos_hint={'x': .25, 'y': .25})
        execute.bind(on_press = self.execute)
        command_layout.add_widget(execute)

        self.add_widget(command_layout)

    def execute (self, *args):
        msg = self.read_text.text
       
        if msg and self.app.connection:
            self.app.connection.write(msg.encode('utf-8'))
            self.label.text = "Command has been sent.\n Enter command"
            self.read_text.text = ""
        else:
            self.label.text = "Something went wrong.\n Enter command"

    def back (self, *args):
    	self.manager.current = 'main'




if __name__ == "__main__":
    app = MainApp()
    app.run()