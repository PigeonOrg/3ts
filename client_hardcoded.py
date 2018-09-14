#!/usr/bin/env python


import socket
import time

# EDIT: Put your IP here
TCP_IP = '10.0.0.2'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGES = [
    '---------',
    '--X------',
    '-OX------',
    '-OX-X----',
    '-OXOX----',
    '-OXOX-X--'
]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
data = s.recv(BUFFER_SIZE)
player = 1
if data.decode('utf-8') == MESSAGES[0]:
    player = 0
for i in range(1, 6):
    if i % 2 == player:
        continue
    s.send(MESSAGES[i].encode('utf-8'))
    data = s.recv(BUFFER_SIZE)
    print("received data:", data)
time.sleep(1)
s.close()
