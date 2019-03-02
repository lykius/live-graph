import matplotlib.pyplot as plt
from matplotlib import animation
from collections import deque
import socket
import json
import sys

HOST = ''
PORT = 12345
SOCKET_BUFFER_SIZE = 1024
MAX_DEQUE_SIZE = 100
XRANGE = (0, MAX_DEQUE_SIZE)
YRANGE = (0, 40)
REFRESH_PERIOD = 1  # millis

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_connection = ''
client_addr = ''
data = {}


def data_server():
    while True:
        json_msg = client_connection.recv(SOCKET_BUFFER_SIZE)
        msg = json.loads(json_msg.decode())
        label, value = msg['label'], msg['value']
        if label not in data:
            data[label] = deque([0 for _ in range(MAX_DEQUE_SIZE)],
                                MAX_DEQUE_SIZE)
        data[label].append(value)
        client_connection.send('#ACK#'.encode())
        yield data


lines = {}
fig = plt.figure(num='Live Graph')
plt.xlim(XRANGE)
plt.ylim(YRANGE)


def animate(data):
    for label in data:
        if label not in lines:
            new_line, = plt.plot(data[label], label=label)
            lines[label] = new_line
            plt.legend(loc='upper right')
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
            anim = animation.FuncAnimation(fig,
                                           animate,
                                           data_server,
                                           interval=REFRESH_PERIOD,
                                           blit=True)
            plt.show()
except:
    print('Exception:', sys.exc_info()[0], '-', sys.exc_info()[1])
