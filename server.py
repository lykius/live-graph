import matplotlib.pyplot as plt
from matplotlib import animation
from collections import deque
import socket
import json
import sys

HOST = ''
PORT = 12345
MAX_DEQUE_SIZE = 100

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_connection = ''
client_addr = ''

data = {}

def data_server():
    while True:
        json_msg = client_connection.recv(1024)
        msg = json.loads(json_msg.decode())
        label, value = msg['label'], msg['value']
        if label not in data.keys():
            data[label] = deque([0 for n in range(MAX_DEQUE_SIZE)], MAX_DEQUE_SIZE)
        data[label].append(value)
        client_connection.send('#ACK#'.encode())
        yield data

lines = {}
fig = plt.figure()
plt.xlim(0, 100)
plt.ylim(0, 40)

def animate(data):
    for label in data.keys():
        if label not in lines.keys():
            new_line, = plt.plot(data[label], label=label)
            lines[label] = new_line
            plt.legend()
        else:
            lines[label].set_ydata(data[label])
    return [lines[label] for label in lines]

try:
    with server_socket:
        print('Socket created')
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print('Waiting connection...')
        client_connection, client_addr = server_socket.accept()
        print('Accepted connection from', client_addr)
        with client_connection:
            anim = animation.FuncAnimation(fig, animate, data_server, interval=1, blit=True)
            plt.show()
except:
    print('Exception:', sys.exc_info()[0], '-', sys.exc_info()[1])

