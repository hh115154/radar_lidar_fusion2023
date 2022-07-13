import zmq
import time
import numpy as np
import queue as Queue
import ConfigConstantData
import meta_pb2
import common_pb2
import cv2
from google.protobuf.json_format import MessageToDict

import av
import ctypes
from ctypes import *

import os
from PIL import Image
from io import BytesIO




context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://10.13.1.10:5560")# server ip
socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))  # 接收所有消息

meta_obj = meta_pb2.Meta()
commom_pb2_Image = common_pb2.Image

cntr = 0
output_path = 'C:/Users/yangh/Desktop/pic.jpg'

# pcl_alg_dll = CDLL('./cppdll/pcl_alg_dll.dll')
# h265_decoder_dll = CDLL('./cppdll/H265_Decode.dll')
h265_decoder_dll = CDLL('C:/Users/yangh/source/repos/H265_Decode/x64/Release/H265_Decode.dll')


# swscale_dll = CDLL('./cppdll/swscale-5.dll')



codec_context = av.codec.CodecContext.create('hevc','r')

avframe_yuv = av.frame.Frame()


print("start")
while True:

    response = socket.recv()
    # response = response.split(b' ', 1)[1]
    msg_len = len(response)
    print("%d th msg_len is %d:"%(cntr, msg_len))

    print(response[0], response[1], response[2], response[3], response[4])

    if response[0] == 8:
        pass
        # meta_obj.ParseFromString(response)
        # # print("frame_id is:", meta_obj.frame_id)
        # discrptorLen = len(meta_obj.data.data_descriptor)
        # # print(discrptorLen)
        #
        # for i in range(discrptorLen):
        #     data_descriptor = meta_obj.data.data_descriptor[i]
        #     data = data_descriptor.data
        #     # print(data.type,data.proto,data.channel,data.with_data_field)

    elif response[0] == 0:# h265
        buf = np.zeros(ConfigConstantData.pic_width*ConfigConstantData.pic_height*3, dtype=np.uint8)


    elif response[1] == 216: # image info


        img = cv2.imdecode(np.frombuffer(response, np.uint8), cv2.IMREAD_COLOR)
        h = img.shape[0]
        w = img.shape[1]

        data = cv2.resize(img,dsize=(1920,1080),fx=1,fy=1,interpolation=cv2.INTER_LINEAR)
        # img.resize((3840, 2160,3))
        # img.reshape(2160, 3848, 3)
        cv2.imshow('img', data)
        cv2.waitKey(1)


    elif response[0] == 255:
        pass
        # if msg_len == 776:
        #     # print("3th long message len of 776")
        # else:
        #     # print("2th msg" )


    else:
        print(response[0])

    response = []

    cntr += 1
    cntr %= 4
