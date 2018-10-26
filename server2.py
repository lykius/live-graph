import matplotlib.pyplot as plt
from collections import deque
import socket
import json
import sys
from multiprocessing import Lock

HOST = ''
PORT = 12345

data = {}
max_data_size = 100
data_lock = Lock()

lines = {}
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 40))

def log_data(label, value):
    data_lock.acquire()
    try:
        if label not in data.keys():
            data[label] = deque('', max_data_size)
            new_line, = ax.plot([], [], label=label)
            lines[label] = new_line
            plot.legend()
        data[label].append(value)
    finally:
        data_lock.release()

x = [n for n in range(0, 101)]

def animate(i):
    data_lock.acquire()
    try:
        for label in data.keys():
            lines[label].set_data(x, data[label])
    finally:
        data_lock.release()
    return lines.values()

anim = animation.FuncAnimation(fig, animate, interval=100, blit=True)
plt.show(block=False)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Socket created')
        s.bind((HOST, PORT))
        s.listen(1)
        print('Waiting connection...')
        conn, addr = s.accept()
        print('Accepted connection from', addr)
        with conn:
            while True:
                json_msg = conn.recv(1024)
                msg = json.loads(json_msg.decode())
                label, value = msg['label'], msg['value']
                log_data(label, value)
                conn.send('#ACK#'.encode())
except:
    print('Exception:', sys.exc_info()[0], '-', sys.exc_info()[1])
