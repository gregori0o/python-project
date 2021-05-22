class Parser(object):
    def __init__(self):
        pass
    
    
    @property
    def command(self):
        return self._command


    @command.setter
    def command(self, command: str):
        self._command = command.split(sep=' ')


    @property
    def executable(self):
        return self.command[0]


    @executable.setter
    def executable(self, command: str):
        raise TypeError('Parser: Attempt to set executable')

        
    def __call__(self, command: str):
        # cmd = command.split(sep=' ')
        return command.split(sep=' ')


import webbrowser as wb
from pynput.mouse import Button, Controller
from subprocess import PIPE, Popen, STDOUT
import os

class CommandHandler(object):
    def __init__(self):
        self.regular_commands = {
            'shutdown': ['shutdown', '-h', 'now'],
            'volume-up': ['amixer', 'sset', 'Master', '2%+'],
            'volume-down': ['amixer', 'sset','Master', '5%-'],
            'keyboard': ['onboard'],
            'brightness-up': ['echo', 'Echo: brightness-up'],
            'brightness-down': ['echo','Echo: brightness-down']
            
        }
        self.browser_commands = {
            'netflix': 'https://www.netflix.com',
            'youtube': 'https://www.youtube.com'
        }
        self.parser = Parser()
        self.mouse = Controller()


    def handle(self, command: str):
        cmd = self.parser(command)
        if cmd[0] == 'cmd':
            if cmd[1] in self.browser_commands.keys():
                wb.open(self.browser_commands[cmd[1]], 1)
                print (self.browser_commands[cmd[1]])
            elif cmd[1] in self.regular_commands.keys():
                Popen(self.regular_commands[cmd[1]], stdout=PIPE)
            else:
                print("CommandHandler: invalid command")
        elif cmd[0] == 'ccmd':
            try:
                print(f'Executing: {cmd[1:]}')
                process = Popen(cmd[1:], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                print(f"Output: {stdout.decode('utf-8')}")
            except Exception:
                print("Popen failed")
        elif cmd[0] == 'mouse':
            if cmd[1] == 'left':
                self.mouse.press(Button.left)
                self.mouse.release(Button.left)
            elif cmd[1] == 'right':
                self.mouse.press(Button.right)
                self.mouse.release(Button.right)
            elif cmd[1] == 'vector':
                ratio = 1500
                x = float(cmd[2]) * ratio
                y = float(cmd[3]) * ratio
                self.mouse.move(x, y)
            else:
                print("CommandHandler: invalid command")
        else:
            raise ValueError("CommandHandler: invalid command descriptor", cmd[0])