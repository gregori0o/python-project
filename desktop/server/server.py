import socket as sc
import logging as lg
import os

class Server(object): 
    def __init__(self, max_connections: int = 1):
        self.logger             = lg.getLogger(__name__)
        # self.logger.setLevel()
        
        # domyślnie dopuszczamy tylko jedno połączenie jednocześnie
        self.max_connections: int = max_connections
        
        self.host_name: str     = sc.gethostname()
        
        # na maszynach z hostem lokalnym zdefiniowanym w /etc/hosts zwraca 
        # self-loop adres (zwykle 127.0.0.1)
        # self.ip4_address: str   = sc.gethostbyname(self.host_name)

        # będzie działać co najmniej na systemach unixowych, ponieważ polecenie
        # `hostname` bazuje na wywołuaniu systemowym gethostname() z unistd.h
        self.ip4_address: str   = os.popen('hostname -I').read()
        
        self.socket: sc.socket  = None
        self.port: int          = 0       
        self.connection         = None
        self.connection_address = None
        
        self.logger.debug('Created Server object, specs:\n%s' % (str(self)))
        
        
    def __str__(self):
        ret = f'Server configuration: Host name: {self.host_name} IPv4: {self.ip4_address}'
        return ret
        
    def run(self):
        if self.socket is not None:
            self.logger.warning('Rerunning server; ATM: %s' % (str(self)))
        
        self.socket = sc.socket()
        
        # jeżeli self.port == 0 to przydzielony zostanie wolny port wybrany przez system
        self.socket.bind(('', self.port))
        
        _, self.port = self.socket.getsockname()
        
        self.socket.listen(self.max_connections)

        self.connection, self.connection_address = self.socket.accept()
        
        self.logger.info('%s initialized connection with server (%s, %s)' % (self.connection, self.ip4_address, self.port))
        
        
        
        
        
    



if __name__ == '__main__':
    print(__name__)
    server = Server()
    
    server.run()
    print(server)
    