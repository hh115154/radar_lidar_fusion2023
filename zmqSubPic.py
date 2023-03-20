import zmq
import cv2
import numpy as np


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))  # 接收所有消息

while True:
    response = socket.recv()
    print("response len is:", len(response))

    nparr = np.asarray(bytearray(response), dtype="uint8")
    img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow('Main Camera', img_decode)

    cv2.waitKey(1)
