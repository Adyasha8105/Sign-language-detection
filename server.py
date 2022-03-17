import socket 
import cv2
import mediapipe as mp
import codecs
import sys 
import pickle
import numpy as np
import struct 
from tensorflow.keras.models import load_model

HOST = '127.0.0.1'
PORT = 9000

model = load_model('mp_hand_gesture')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(10)
print("Socket connection is open")

conn, addr = s.accept()

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

x = 480 
y = 640 
c = 3

cap = cv2.VideoCapture(0)
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

data = b""
payload_size = struct.calcsize("s")
while True:
    _, frame = cap.read()
    while len(data) < payload_size: 
        data  += conn.recv(4096)
        data = data.decode()
        data = list(data.split('\n'))

        if data:
            landmarks = []
            for handslms in data:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                classID = np.argmax(prediction)
                className = classNames[classID]

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("s", packed_msg_size)[0]
    # while len(data) < msg_size: 
    #     data += conn.recv(4096)
    # frame_data = data[:msg_size]
    # data = data[msg_size:]