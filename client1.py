import socket
import time

def make_request():
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    sock.send(b'GET /\n\n')
    resp = sock.recv(100)
    sock.close()
    end_time = time.time()
    print(end_time-start_time)

while True:
    make_request()
