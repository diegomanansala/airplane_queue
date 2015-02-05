import socket
import thread

import Queue

LOW_PRIO_QUEUE_PORT = 12345
STANDARD_PRIO_QUEUE_PORT = 12346
HIGH_PRIO_QUEUE_PORT = 12347
CONSUMPTION_SERVER = 12348

hQueue = Queue.Queue(5)
workQueue = Queue.Queue(10)
lQueue =  Queue.Queue(2)

"""
	Assumptions:
	- Runways are in segregated mode i.e. one runway is always for arrivals while another runway is always for departures
"""

# set port for each process queues
FLYING_QUEUE_PORT = 12344
LANDING_QUEUE_PORT = 12345
LANDING_TAXIING_QUEUE_PORT = 12346
UNLOADING_QUEUE_PORT = 12347
BOARDING_QUEUE_PORT = 12348
TRANSFER_TAXIING_QUEUE_PORT = 12349
MAINTENANCE_QUEUE_PORT = 12350
TAKEOFF_TAXIING_QUEUE_PORT = 12351
TAKEOFF_QUEUE_PORT = 12352
PASSENGER_QUEUE_PORT = 12353
AIRPORT_CONSUMPTION_SERVER = 12354

# variables
airplanes = 1
runways = 1
passengers = 150
terminals = 3
gates_per_terminal = 10
taxiing_lanes = 10
maintenance = 3

# initialize queues
flyingQueue = Queue.Queue(airplanes);
landingQueue = Queue.Queue(runways);
taxiLandingQueue = Queue.Queue(taxiing_lanes);
unloadingQueue = Queue.Queue();
boardingQueue = Queue.Queue();
taxiTransferQueue = Queue.Queue();
maintenanceQueue = Queue.Queue(maintenance);
taxiTakeoffQueue = Queue.Queue(taxiing_lanes);
takeoffQueue = Queue.Queue(runways);
passengerQueue = Queue.Queue(passengers);

def consumption_server(port):

    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, port))

    s.listen(1)
    while True:
        c, addr = s.accept() 
        if hQueue.qsize() > 0:
            data = hQueue.get(0)
            c.send(data)
        elif workQueue.qsize() > 0:
            data = workQueue.get(0)
            c.send(data)
        elif lQueue.qsize() > 0:
            data = lQueue.get(0)
            c.send(data)
        c.close()

def start_queue_server(port, tQueue):

    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, port))

    s.listen(1)
    while True:
        c, addr = s.accept()
        if not tQueue.full():
            data = c.recv(1024)
            tQueue.put(data)
            print 'Queued: ' + data + ' ' + str(lQueue.qsize()) + ' ' + str(workQueue.qsize()) + ' ' + str(hQueue.qsize())
        else:
            print 'Cannot accommodate ' + data + '. Queue is full.'
        c.close()

thread.start_new_thread( start_queue_server, (LOW_PRIO_QUEUE_PORT, lQueue) )
thread.start_new_thread( start_queue_server, (STANDARD_PRIO_QUEUE_PORT, workQueue) )
thread.start_new_thread( start_queue_server, (HIGH_PRIO_QUEUE_PORT, hQueue) )
thread.start_new_thread( consumption_server, (CONSUMPTION_SERVER,) )

while True:
    pass