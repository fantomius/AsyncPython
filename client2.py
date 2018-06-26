import socket
import time
from threading import Thread

def make_request():
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    sock.send(b'GET /\n\n')
    resp = sock.recv(100)
    sock.close()
    end_time = time.time()
    print(time.strftime("%H:%M:%S"), end_time-start_time)

from threading import Thread

def do_request_forever():
    while True:
        make_request()

t1 = Thread(target=do_request_forever)
t2 = Thread(target=do_request_forever)

t1.start()
t2.start()
