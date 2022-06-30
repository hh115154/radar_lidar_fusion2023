import zmq
import time
import numpy as np
import meta_pb2
import common_pb2
import cv2
from google.protobuf.json_format import MessageToDict
import ffmpeg
import av

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://10.13.1.10:5560")# server ip
socket.setsockopt(zmq.SUBSCRIBE, ''.encode('utf-8'))  # 接收所有消息

meta_obj = meta_pb2.Meta()
commom_pb2_Image = common_pb2.Image

cntr = 0
output_path = 'C:/Users/yangh/Desktop/pic.jpg'


while True:

    response = socket.recv()
    # response = response.split(b' ', 1)[1]
    msg_len = len(response)
    # print("%d th msg_len is %d:"%(cntr, msg_len))

    # print(response[0], response[1], response[2], response[3], response[4])
    if response[0] == 8:
        meta_obj.ParseFromString(response)
        print("frame_id is:", meta_obj.frame_id)
        # print('image is:', meta_obj.data.image)
    elif response[0] == 0: # image info
        # print("1th long message len of ")
        commom_pb2_Image = meta_obj.data.image[0] # 重要，用下标将数据冲容器里拿出来

        # print("image counter is:", commom_pb2_Image.image_counter)

        width = commom_pb2_Image.width
        height = commom_pb2_Image.height
        sub_sample = commom_pb2_Image.send_mode
        color_mode = commom_pb2_Image.format

        # print('color_mode is:', color_mode)



        #
        # fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
        # fps = int(17)
        # vw = cv2.VideoWriter(output_path, fourcc, fps, (width, height), True)


        if (color_mode == common_pb2.ImageFormat.TIMEOUT):
            pass
           #this is a fake image when camera interrupt timeout happened
        else:

            image = np.asarray(bytearray(response), dtype="uint8")
            # image = cv2.imdecode(image, cv2.IMREAD_COLOR) # 0 灰度图
            # print(image.a)
            av.frame = image
            av.codec = av.avcodec_find_decoder(av.AV_CODEC_ID_H264)
            av.buffer = response



            # print("image shape is:", image)


            # image = cv2.imread(output_path,0) #test source

            # cv2.imshow("Hello", image)
            # cv2.waitKey(0)
            # cv2.destoryAllWindows()

            # image = cv2.cvtColor(image, cv2.IMREAD_COLOR)
            #
            # cv2.imshow('frame', image)
            # cv2.waitKey(5)

        #
        #     cv2.imwrite("result.jpg", image)
        #
        #     cv2.imshow("Hello", image)
        #
        #     if cv2.waitKey(10000) & 0xFF == ord('q'):
        #         cv2.destroyAllWindows()

    elif response[0] == 255:
        pass
        # if msg_len == 776:
        #     # print("3th long message len of 776")
        # else:
        #     # print("2th msg" )

    response = []

    cntr += 1
    cntr %= 4
