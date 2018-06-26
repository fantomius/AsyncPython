import socket
import time
from select import select
from threading import Thread
from collections import deque

class EventLoop:
    def __init__(self):
        self.tasks = deque()
        self.stopped = {}

    def add_task(self, task):
        self.tasks.append(task)

    def add_future(self, future):
        self.tasks.append(future.monitor())

    def run_forever(self):
        while any([self.tasks, self.stopped]):
            while not self.tasks:
                ready_to_read, _, _ = select(self.stopped.keys(), [], [], 1.0)
                for r in ready_to_read:
                    self.tasks.append(self.stopped.pop(r))
            while self.tasks:
                task = self.tasks.popleft()
                try:
                    sock = next(task)
                    self.stopped[sock] = task
                except StopIteration:
                    pass

class AsyncSocket(socket.socket):
    def AsyncRead(self, capacity=100):
        yield self
        return self.recv(100)

class Future:
    def __init__(self, done_callback):
        self.notify, self.event = socket.socketpair()
        self.done_callback = done_callback
        self.result = None

    def set_done(self, result):
        self.result = result
        self.notify.send(b'done')
        self.done_callback(self.result)

    def monitor(self):
        yield self.event
        self.event.recv(100)


def make_request():
    start_time = time.time()
    sock = AsyncSocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    sock.send(b'GET /\n\n')
    resp = yield from sock.AsyncRead(100)
    sock.close()
    end_time = time.time()
    print(time.strftime("%H:%M:%S"), end_time-start_time)

ev = EventLoop()

def future_producer():
    while True:
        f = Future(lambda x: ev.add_task(make_request()))
        ev.add_future(f)
        time.sleep(1.0)
        f.set_done(1.0)

t = Thread(target=future_producer)
t.start()

ev.run_forever()


