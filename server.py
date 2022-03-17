import socket 
import codecs
import sys 
import pickle
import numpy as np
import struct 

HOST = '127.0.0.1'
PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(10)
print("Socket connection is open")

conn, addr = s.accept()

data = b""
payload_size = struct.calcsize("s")
while True:
    while len(data) < payload_size: 
        data  += conn.recv(4096)
        if len(data) > 0: 
            print(bytes(str(data), 'UTF-8'))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("s", packed_msg_size)[0]
    # while len(data) < msg_size: 
    #     data += conn.recv(4096)
    # frame_data = data[:msg_size]
    # data = data[msg_size:]