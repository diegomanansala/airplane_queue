import socket
import thread
import time
from random import randrange

LOW_PRIO_QUEUE_PORT = 12345
STANDARD_PRIO_QUEUE_PORT = 12346
HIGH_PRIO_QUEUE_PORT = 12347

def connect_to_server(threadName, port, interarrivalTime):

    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    s.send(threadName)    
    print threadName + ' with interarrival time ' + str(interarrivalTime) + 's'
    s.close 

# Create two threads as follows
counter = 0

while 1:

	try:
		while True:
			delay = 1.5
			time.sleep(delay)
			randQueueId = randrange(10)
			print "randQueueId",randQueueId
			if randQueueId < 4:
				thread.start_new_thread( connect_to_server, ("Low Customer", LOW_PRIO_QUEUE_PORT, delay+15) )
			elif randQueueId > 3 and randQueueId < 7:
				thread.start_new_thread( connect_to_server, ("Standard Customer", STANDARD_PRIO_QUEUE_PORT, delay+1) )
			else:
				thread.start_new_thread( connect_to_server, ("High Customer", HIGH_PRIO_QUEUE_PORT, delay+10) )
			
			counter += 1
            
	except:
		pass

	if(counter>20):
		break
