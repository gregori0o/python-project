from queue import Queue
import socket as sc
import sys
import os
from typing import Callable

class Server(object): 
    def __init__(   self, 
                    max_connections: int = 1, 
                    buffer_size: int = 1024, 
                    client_input_handler = None, 
                    server_answer_handler = None):
        # self.logger.setLevel()
        
        # on default only 1 connection is allowed 
        self.max_connections: int = max_connections
        self.buffer_size: int   = buffer_size
        
        self.host_name: str     = sc.gethostname()
        
        # on machines with local host defined in  /etc/hosts it returns
        # self-loop adres (127.0.0.1)
        # self.ip4_address: str   = sc.gethostbyname(self.host_name)

        # works on unix machines; underneath it relies on gethostname() syscall
        # from unistd.h
        self.ip4_address: str   = os.popen('hostname -I').read()
        
        self.socket: sc.socket  = sc.socket(family=sc.AF_INET, type=sc.SOCK_STREAM)
        self.port: int          = 0       
        self.connection         = None
        self.connection_address = None
        
        # self.port == 0 ==> system automatically assignes port number
        # '' ==> socket is not binded to particular host (if hostname was passed, socket would be 
        # bound to self-loop address preventing any conneciton from remote clients)
        self.socket.bind(('', self.port))
        
        _, self.port = self.socket.getsockname()

        self.socket.listen(self.max_connections)
        
        if client_input_handler is not None: self.input_handler = client_input_handler
        else: self.input_handler = self.handle_input
        
        if server_answer_handler is not None: self.answer_handler = server_answer_handler
        else: self.answer_handler = self.handle_answer
        

    def __str__(self):
        return 'Server:\n\tHostname: %s\n\tIPv4: %s\tPort: %s' % (self.host_name, self.ip4_address, self.port)
        

    def wait_for_connection(self):
        if self.socket is None:
            raise UnboundLocalError('Waiting for connection with null socket')

        self.connection, self.connection_address = self.socket.accept()


    def handle_connection(self):
        if self.connection is None:
            raise UnboundLocalError('Handling null connection')
        
        while True:
            received_data = self.connection.recv(self.buffer_size).decode()

            if not received_data:
                break

            self.input_handler(received_data)

            answer = self.answer_handler(received_data)

            self.connection.send(answer.encode())

        self.close_connection()
         

    def handle_input(self, data: str):
        print("Received from client: ", data)

    
    def handle_answer(self, data: str):
        return "Server answer for " + data 


    def close_connection(self):
        if self.connection is None:
            self.logger.warning('Closing null connection')
            return

        self.logger.info('Closing connection with %s' % (str(self.connection.getsockname())))
        self.connection.close()
        
    def run(self, queue: Queue):
        while True:
            self.wait_for_connection()
            queue.put(None)
            self.handle_connection()

    
        
        
if __name__ == '__main__':
    print(__name__)
    server = Server()

    while True:
        server.wait_for_connection()
        print("czekam na polacznenie...")
        server.handle_connection()

    # server.close_connection()

    print(server)
    