import zmq
import time
import numpy as np
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


swscale_dll = CDLL('./cppdll/swscale-5.dll')



codec_context = av.codec.CodecContext.create('hevc','r')

avframe_yuv = av.frame.Frame()


print("start")
while True:

    response = socket.recv()
    # response = response.split(b' ', 1)[1]
    msg_len = len(response)
    # print("%d th msg_len is %d:"%(cntr, msg_len))

    # print(response[0], response[1], response[2], response[3], response[4])




    if response[0] == 8:
        meta_obj.ParseFromString(response)
        # print("frame_id is:", meta_obj.frame_id)
        discrptorLen = len(meta_obj.data.data_descriptor)
        # print(discrptorLen)

        for i in range(discrptorLen):
            data_descriptor = meta_obj.data.data_descriptor[i]
            data = data_descriptor.data
            # print(data.type,data.proto,data.channel,data.with_data_field)
            bWithDataField = data.with_data_field

    elif response[0] == 0: # image info

        bUseDll = True

        print("1th long message len of-------------------------------- ")

        print("frame_id is:", meta_obj.frame_id)
        commom_pb2_Image = meta_obj.data.image[0] # 重要，用下标将数据冲容器里拿出来

        width = commom_pb2_Image.width
        height = commom_pb2_Image.height
        sub_sample = commom_pb2_Image.send_mode
        color_mode = commom_pb2_Image.format
        resp_list = list(response)
        if bUseDll:





            resp_type = ctypes.c_char_p * len(resp_list)
            arg_resp = resp_type(*resp_list)

            my_h265_decode = h265_decoder_dll.decode_h265
            my_h265_decode.argtypes = [POINTER(c_char_p), ctypes.c_ulong,ctypes.c_int32,ctypes.c_int32]
            # my_h265_decode.restype =POINTER(c_char)

            print("before call  cpp dll___________")
            my_h265_decode(arg_resp, len(response), width, height)
            print("after call  cpp dll___________")
            res_list = []
        else:
            avpkt_h265 = av.packet.Packet(response)#av.packet.Packet()
            codec_context.width = width
            codec_context.height = height
            # avpkt_h265.decode_one()


            # av.stream.Stream.decode(avpkt_h265)

            frame =  codec_context.decode(avpkt_h265)
            # avframe_yuv = codec_context.receive()
            cv2.imshow("Test", frame)


            #
            # ndArray = np.frombuffer(response[1:], dtype=np.uint8)
            # ndArray = ndArray.reshape(height, width, 3)
            # frame = av.video.frame.VideoFrame.from_ndarray(ndArray,'rgb24')

        # try:
        #     for i in range(width*height):
        #         res_list.append(res[i])
        #
        #     # print(res_list)
        # except Exception as e:
        #     print(e)
        #     continue

        # response1 = np(response).reshape(height, width, cv2.CV_8UC3)
        #
        # sws_ctx = ffmpeg.libswscale.sws_getContext(width, height, color_mode, width, height, ffmpeg.libavutil.AV_PIX_FMT_BGR24,ffmpeg.libswscale.SWS_BICUBIC, None, None, None)
        #
        # # int cvLinesizes = mat.step1();
        # #
        # # ffmpeg.libswscale.sws_scale(sws_ctx, response, commom_pb2_Image.linesize, 0, height,
        #
        #
        # cv2.imshow("Hello", res)

        # method1
        # try:
        #     img = bytearray(response).to_nd_array(format='bgr25')
        #     cv2.imshow("Test", img)
        # except Exception as e:
        #     print('fate erro:{}'.format(e))
        # cv2.destroyAllWindows()

        # method2
        # container = av.open(response, format="h264", mode='r')
        # cur_pos = 0
        # while True:
        #     data = await websocket.recv()
        # rawData.write(data)
        # response.seek(cur_pos)
        # for packet in container.demux():
        #     if packet.size == 0:
        #         continue
        #     cur_pos += packet.size
        # Frame = []
        # for frame in packet.decode():
        #     Frame.append(frame)
        #
        # cv2.imshow("Test", Frame)

        # method3
        # while True:
        #     try:
        #         frame = av.codec.(response, format="h265", streams=1)
        #         # frame = np.fromstring(av.b64decode(commom_pb2_Image), dtype=np.uint8)
        #         cv2.imshow("Frame",frame)
        #         # show the frame to our screen
        #         cv2.waitKey(1) # Display it at least one ms # # before going to the next frame
        #     except KeyboardInterrupt:
        #         cv2.destroyAllWindows()
        #         break



    elif response[0] == 255:
        pass
        # if msg_len == 776:
        #     # print("3th long message len of 776")
        # else:
        #     # print("2th msg" )

    response = []

    cntr += 1
    cntr %= 4
