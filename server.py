import matplotlib.pyplot as plt
from time import sleep
from collections import deque
import socket
import json
import sys

plt.ion()

data = {}
max_data_size = 100

HOST = ''
PORT = 12345

def log_data(label, value):
    if label not in data.keys():
        data[label] = deque('', max_data_size)
    data[label].append(value)


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Socket created')
        s.bind((HOST, PORT))
        s.listen(1)
        print('Waiting connection...')
        conn, addr = s.accept()
        print('Accepted connection from', addr)
        with conn:
            plot_lines = {}
            colors = ['g-', 'r-', 'b-']
            label_colors = {}
            plt.axis([0, 100, 0, 40])
            while True:
                json_msg = conn.recv(1024)
                msg = json.loads(json_msg.decode())
                label, value = msg['label'], msg['value']
                log_data(label, value)
                conn.send('#ACK#'.encode())
                if label not in label_colors.keys():
                    label_colors[label] = colors.pop()
                if label in plot_lines.keys():
                    for line in plot_lines[label]:
                        line.remove()
                plot_lines[label] = plt.plot(data[label], label_colors[label], label=label)
                plt.legend()
                plt.pause(0.0001)
except:
    print('Exception:', sys.exc_info()[0], '-', sys.exc_info()[1])

