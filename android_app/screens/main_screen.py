from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup


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

        self.button_l1 = Button(text="Brightness UP",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .79})
        self.button_l1.bind(on_press = self.execute_buttons)
        main_layout.add_widget(self.button_l1)
        self.button_r1 = Button(text="Volume UP",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .79})
        self.button_r1.bind(on_press = self.execute_buttons)
        main_layout.add_widget(self.button_r1)
        self.button_l2 = Button(text="Brightness DOWN",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .68})
        self.button_l2.bind(on_press = self.execute_buttons)
        main_layout.add_widget(self.button_l2)
        self.button_r2 = Button(text="Volume DOWN",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .68})
        self.button_r2.bind(on_press = self.execute_buttons)
        main_layout.add_widget(self.button_r2)
        self.button_l3 = Button(text="Shutdown",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .57})
        self.button_l3.bind(on_press = self.execute_buttons)
        self.yes = None
        main_layout.add_widget(self.button_l3)
        self.button_r3 = Button(text="Keyboard",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .57})
        self.button_r3.bind(on_press = self.execute_buttons)
        main_layout.add_widget(self.button_r3)
        self.button_l4 = Button(text="NETFLIX",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .0, 'y': .46})
        self.button_l4.bind(on_press = self.execute_buttons)
        main_layout.add_widget(self.button_l4)
        self.button_r4 = Button(text="YOUTUBE",
                      halign='center',
                      size_hint=(.4, .1),
                      pos_hint={'x': .6, 'y': .46})
        self.button_r4.bind(on_press = self.execute_buttons)
        main_layout.add_widget(self.button_r4)
        mouse = TouchPad (app, size_hint=(1, .4),
                      pos_hint={'x': .0, 'y': .0})
        main_layout.add_widget(mouse)

        self.add_widget(main_layout)

    def exit (self, *args):
      if self.app.connection:
        self.app.connection.write("cmd disconnect".encode('utf-8'))
        self.app.connection = None
      self.manager.current = 'start'

    def command (self, *args):
    	self.manager.current = 'command'

    def popup (self):
    	layout = FloatLayout()
    	label = Label (text="Are you sure to shutdown the computer?",
    				  halign='center',
                      font_size='20sp',
                      size_hint=(1, .2),
                      pos_hint={'x': 0, 'y': 0.7})
    	layout.add_widget(label)
    	self.yes = Button (text="YES",
    				  halign='center',
    				  size_hint=(1., .3),
                      pos_hint={'x': .0, 'y': .35})
    	self.yes.bind(on_press = self.execute_buttons)
    	layout.add_widget(self.yes)
    	no = Button (text="NO",
    				  halign='center',
    				  size_hint=(1., .3),
                      pos_hint={'x': .0, 'y': .0})
    	layout.add_widget(no)

    	popup = Popup (title="WARNING!",
    				  title_align='center',
    				  content=layout,
    				  size_hint=(1, 1),
    				  auto_dismiss=False)
    	no.bind(on_press = popup.dismiss)
    	popup.open()


    def execute_buttons (self, button, *args):
      if not self.app.connection:
        return
      if button == self.button_l1:
        self.app.connection.write("cmd brightness-up".encode('utf-8'))
      elif button == self.button_r1:
        self.app.connection.write("cmd volume-up".encode('utf-8'))
      elif button == self.button_l2:
        self.app.connection.write("cmd brightness-down".encode('utf-8'))
      elif button == self.button_r2:
        self.app.connection.write("cmd volume-down".encode('utf-8'))
      elif button == self.button_l3:
        self.popup()
      elif button == self.yes:
        self.app.connection.write("cmd shutdown".encode('utf-8'))
      elif button == self.button_r3:
        self.app.connection.write("cmd keyboard".encode('utf-8'))
      elif button == self.button_l4:
        self.app.connection.write("cmd netflix".encode('utf-8'))
      elif button == self.button_r4:
        self.app.connection.write("cmd youtube".encode('utf-8'))


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
                      size_hint=(.6, .2),
                      pos_hint={'x': .2, 'y': 0.7})
        command_layout.add_widget(self.label)
        self.read_text = TextInput(
                      multiline=True,
                      readonly=False,
                      halign="left",
                      font_size='20sp',
                      size_hint=(.8, .3),
                      pos_hint={'x': .1, 'y': 0.4})
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
            self.app.connection.write(("ccmd " + msg).encode('utf-8'))
            self.label.text = "Command has been sent.\n Enter command"
            self.read_text.text = ""
        else:
            self.label.text = "Something went wrong.\n Enter command"

    def back (self, *args):
    	self.manager.current = 'main'
