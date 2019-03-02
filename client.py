import socket
import json
import sys
import random

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
SOCKET_BUFFER_SIZE = 1024

data = {}
data['data1'] = 5
data['data2'] = 10
data['data3'] = 15
data['data4'] = 20
data['data5'] = 25

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Socket created')
        print('Connecting to server...')
        s.connect((SERVER_HOST, SERVER_PORT))
        print('Connected')
        while True:
            for label in data:
                msg = {
                    'label': label,
                    'value': data[label] + (random.random() * 6 - 3)
                }
                json_msg = json.dumps(msg)
                s.send(json_msg.encode())
                ack = s.recv(SOCKET_BUFFER_SIZE)
except:
    print('Exception:', sys.exc_info()[0], '-', sys.exc_info()[1])
