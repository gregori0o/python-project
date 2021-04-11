""" Desktop application """

import threading
import queue
from kivy import app
from window.appwindow import *
from server.server import Server


def main():
    """ 
    1. Creation of server object. 
    2. Collection of server data (hostname, ip, port). 
    3. Starting server on parallel thread. 
    4. Starting window window application.  
    """

    thread_queue = queue.Queue(maxsize=4)

    app_server          = Server()    
    server_ip           = app_server.ip4_address
    server_port         = app_server.port
    server_host_name    = app_server.host_name

    print(server_host_name, server_ip, server_port)
    
    application = Application()
    
    
    
    
    thread_1 = threading.Thread(target=app_server.run, args=(thread_queue,)) 
    
    
    
    thread_2 = threading.Thread(target=application.start)
    
    
    print('Starting server in background...')
    thread_1.start()
    
    print('Starting application window...')
    thread_2.start()
    
    
    
    thread_2.join()
    # application window is not closing for unknown (yet) reasons, while thread_2 joins
    # main thread??
    print('thread_2 exited')
    thread_1.join()

    return 0
    

    
if __name__ == '__main__':
    main()
    