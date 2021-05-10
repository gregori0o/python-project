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
from subprocess import PIPE, Popen

class CommandHandler(object):
    def __init__(self):
        self.regular_commands = {
            'shutdown': ['shutdown', '-h', 'now'],
            'volume-up': ['aamixer', 'sset', 'Master', '2%+'],
            'volume-down': ['aamixer, sset' ,'Master', '5%-'],
            'onboard': ['onboard']
        }
        self.browser_commands = {
            'netflix': 'www.netflix.com',
            'youtube': 'www.youtube.com'
        }
        self.parser = Parser()


    def handle(self, command: str):
        cmd = self.parser(command)
        if cmd[0] == 'cmd':
            if cmd[1] in self.browser_commands.keys():
                wb.open(self.browser_commands[cmd[1]], 1)
            elif cmd[1] in self.regular_commands.keys():
                Popen(self.regular_commands[cmd[1]], stdout=PIPE)
            else:
                print("CommandHandler: invalid command")
        elif cmd[0] == 'ccmd':
            Popen([command], stdout=PIPE)
        else:
            raise ValueError("CommandHandler: invalid command descriptor", cmd[0])