from random import randrange

import socket
import time

CONSUMPTION_SERVER = 12348

while True:
    
    time.sleep(randrange(1)+2)
    
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, CONSUMPTION_SERVER))
    print 'Processed: ' + str( s.recv(1024) )
    s.close()




