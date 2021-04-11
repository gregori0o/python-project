import socket as sck
from sys import exit


def get_port(path: str) -> int: 
    return int(input('Insert port: '))



hostname = sck.gethostname()

port = get_port('./socket_number.txt')

if not port:
    print('Could not read port number.')
    exit(1)


csocket = sck.socket()
csocket.connect((hostname, port))

message = input('Client>')

while message.lower().strip() != 'end':
    csocket.send(message.encode())
    received_data = csocket.recv(1024).decode()
    print('From server: ' + received_data)
    message = input ("Client>")
    
csocket.close()