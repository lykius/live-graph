import matplotlib.pyplot as plt
from matplotlib import animation
from collections import deque
import socket
import json
import sys
from multiprocessing import Lock, Process
from pprint import pprint

HOST = ''
PORT = 12345

data = {}
max_data_size = 100
data_lock = Lock()

def log_data(label, value):
    data_lock.acquire()
    print('log_data')
    pprint(data)
    try:
        if label not in data.keys():
            data[label] = deque('', max_data_size)
        data[label].append(value)
    finally:
        data_lock.release()

x = [n for n in range(0, 101)]
lines = {}
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 40))

def animate(i):
    data_lock.acquire()
    print('animate')
    pprint(lines)
    pprint(data)
    try:
        for label in data.keys():
            if label not in lines.keys():
                new_line, = ax.plot(x, data[label], label=label)
                lines[label] = new_line
                plt.legend()
            else:
                lines[label].set_data(x, data[label])
    finally:
        data_lock.release()
    return lines.values()

anim = animation.FuncAnimation(fig, animate, interval=1000, blit=True)

def proc():
    plt.show()

p = Process(target=proc)
p.start()

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

