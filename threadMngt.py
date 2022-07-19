# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'

# @Time     : 2022/6/25 15:03

import time
import struct
import cv2
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QWaitCondition, QMutex, QDateTime
import os
import re
import presentationLayer
from mySocket import MyUdpSocket, zmq_sub_client_socket
import protocol
import procAsamMdf
# import CppApi
import logFileMngt
import ConfigConstantData
import protobuf_if
from datetime import datetime

import my_util

import all_data_pb2


class BaseThread(QThread):
    def __init__(self, _bOnLineRecvMode=True):
        super(BaseThread, self).__init__()
        self.mutex = QMutex()
        self.cond = QWaitCondition()
        self._isPause = True
        self.bLoggingFile = False
        self.log_this_frame = False
        self.recv_message = None
        self.log_file = ''
        self.todo_mark = False
        self.bOnLineRecvMode = _bOnLineRecvMode

    def get_next_frame_info(self):
        if self.bOnLineRecvMode:
            self.recv_message = self.socket.client_socket.recv()
        else:
            self.recv_message = self.log_file.get_curr_frame()

            self.log_file.next_frame()


    def log_a_frame_to_file_as_a_line(self, frame):
        strData = my_util.get_timestamp_str() + ' ' + frame.hex(' ') + '\n'
        if self.todo_mark:
            strData = ConfigConstantData.mark_line_head + strData
            self.todo_mark = False
        self.log_file.write(strData)
        self.log_this_frame = False

    def pause(self):
        self._isPause = True

    def resume(self):
        self._isPause = False
        self.cond.wakeAll()

# def run(self) -> None:
# 	while 1:
# 		self.mutex.lock()
# 		if self._isPause:
# 			self.cond.wait(self.mutex)
# 		self.mutex.unlock()


class VideoRecordThread(BaseThread):  # show and record camera
    def __init__(self, _bOnLineRecvMode=True):
        super(VideoRecordThread, self).__init__(_bOnLineRecvMode)
        self.videoFileName = self.getVideoFileName()

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
        self.inpSize = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                        int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        inp_fps = int(self.cap.get(cv2.CAP_PROP_FPS))  # 摄像头原始帧率30
        self.outpSize = (int(400), int(300))
        if inp_fps < 30:
            inp_fps = 30
        self.inpFps = inp_fps
        self.intervalFrmNr = int(6)
        self.outpFps = self.inpFps / self.intervalFrmNr  # f(inpFps,intervalFrmNr)
        self.videoWriter = cv2.VideoWriter(self.videoFileName, self.fourcc, self.outpFps, self.outpSize)
        self.ret, self.frame = self.cap.read()
        self.outpFrame = self.frame
        self.showImage = 0

    def run(self):
        frame_nr = 0
        while self.ret and self.isRunning():
            self.mutex.lock()
            if self._isPause:
                self.cond.wait(self.mutex)

            print("VideoRecordThread is running")
            self.ret, self.frame = self.cap.read()
            try:
                show = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
                frame_nr = frame_nr + 1
                self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                              QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式

                if frame_nr % int(self.intervalFrmNr) == 0:
                    self.outpFrame = cv2.resize(self.frame, self.outpSize)
                    self.videoWriter.write(self.outpFrame)
                    print("running Recording thread and save frame with number of %s", frame_nr)
            except Exception as e:
                print(e)

            self.mutex.unlock()

    def getVideoFileName(self):
        now = QDateTime.currentDateTime()
        now_str = now.toString("yyyyMMdd_hhmmss")
        file_name = now_str + ".mp4"
        return file_name

    def quit(self):
        super(VideoRecordThread, self).quit()
        self.cap.release()
        self.videoWriter.release()
        cv2.destroyAllWindows()

    def saveVideo(self):
        self.videoWriter.release()
        self.videoWriter = None

    def updateVideoWriter(self):
        self.videoFileName = self.getVideoFileName()
        self.videoWriter = cv2.VideoWriter(self.videoFileName, self.fourcc, self.outpFps, self.outpSize)


class OriginalRadarThread(BaseThread):  # 原始雷达图线程,在线采集
    pcl_posn_signal = pyqtSignal(list)
    orgRadar_pcl_signal = pyqtSignal(dict)
    orgRadar_obj_signal = pyqtSignal(list)
    orgRadar_objInfo_signal = pyqtSignal(list)
    Radar2D_obj_signal = pyqtSignal(list)
    fused_objList_signal = pyqtSignal(list, list)

    def __init__(self, _bOnLineRecvMode=True):
        super(OriginalRadarThread, self).__init__(_bOnLineRecvMode)

        if ConfigConstantData.MachineType == ConfigConstantData.radar4D_548:
            self.socket = MyUdpSocket()
        elif ConfigConstantData.MachineType == ConfigConstantData.J3System:
            self.socket = zmq_sub_client_socket(ConfigConstantData.J3C_socket_if)

        self.frmNr = 0
        self.mdf = procAsamMdf.MdfFile()
        self.timestamp = time.time()
        self.presentationPCL = presentationLayer.Pcl_Color()
        self.counter = 0

    def get_next_frame_info(self):
        if self.bOnLineRecvMode:
            self.recv_message = self.socket.client_socket.recv()
        else:
            self.recv_message = self.log_file.get_frame_by_timestamp(self.timestamp)

    def resume1(self, timestamp):
        self.timestamp = timestamp
        self._isPause = False
        self.cond.wakeAll()

    def draw_obj(self, data_bytes):
        self.counter += 1
        self.counter %= 20
        obj_buf = data_bytes[16:9385 + 16]
        obj_list = protocol.ARS548_ObjectList(obj_buf)
        objPresentations = obj_list.getPresentationInfo()

        if self.counter == 0:  # reduce the frequency of data showing
            self.orgRadar_objInfo_signal.emit(obj_list.ObjectList_Objects[0:obj_list.ObjectList_NumOfObjects])
        else:
            self.orgRadar_obj_signal.emit(objPresentations)

    def draw_PCL(self, bytes_data):
        buf = bytes_data[16:35305 + 16]
        dList = protocol.ARS548_DetectionList(buf)
        self.presentationPCL = dList.getPresentationPcl()
        self.orgRadar_pcl_signal.emit(self.presentationPCL.dict_hight2color)

    def rece_4DRadar_548_dara(self):
        try:
            self.recv_message, client = self.socket.udp_socket.recvfrom(self.socket.rcvBufLen)
            msg_len = len(self.recv_message)
            # test write log
            # if 50 == len(recv_message):
            # 	data = struct.unpack('>50B', recv_message)
            # 	print("data len 50",data)
            # elif 158 == len(recv_message):
            # 	data = struct.unpack('>158B', recv_message)
            # 	print("data len 158",data)
            # elif 803 == len(recv_message):
            # 	data = struct.unpack('>803B', recv_message)
            # 	print("data len 803",data)
            if ConfigConstantData.ObjListByteNr == msg_len:  # objects
                self.log_this_frame = True
                data = struct.unpack('>9401B', self.recv_message)
                bytes_data = int.from_bytes(data, byteorder='big').to_bytes(ConfigConstantData.ObjListByteNr,
                                                                            byteorder='big')
                self.draw_obj(bytes_data)

            elif ConfigConstantData.PclByteNr == msg_len:  # pcl
                self.log_this_frame = True

                data = struct.unpack('>35336B', self.recv_message)
                bytes_data = int.from_bytes(data, byteorder='big').to_bytes(ConfigConstantData.PclByteNr,
                                                                            byteorder='big')
                self.draw_PCL(bytes_data)
        except Exception as e:
            print(e)

    def rece_J3C_data(self):
        try:
            # self.recv_message = self.socket.client_socket.recv()
            self.get_next_frame_info()

            self.log_this_frame = self.bLoggingFile  # log all frames received if logging
            self.Data = protobuf_if.All_Data(self.recv_message)

            # if len(self.Data.radar_obj_list_draw) > 0:# 使用有效数据更新视图数据
            self.Radar2D_obj_signal.emit(self.Data.radar_obj_list_draw)

            # if len(self.Data.fused_obj_box2D) > 0:
            self.fused_objList_signal.emit(self.Data.fused_obj_box2D, self.Data.fused_obj_box3D)


        except Exception as e:
            print('oranginal radar thread error:', e)

    def run(self) -> None:
        while True:
            self.mutex.lock()
            if self._isPause:
                self.cond.wait(self.mutex)
            print("OriginalRadarThread is running")

            if ConfigConstantData.MachineType == ConfigConstantData.radar4D_548:
                self.rece_4DRadar_548_dara()
            elif ConfigConstantData.MachineType == ConfigConstantData.J3System:
                self.rece_J3C_data()

            if self.bLoggingFile and self.log_this_frame:
                self.log_a_frame_to_file_as_a_line(self.recv_message)
                if self.todo_mark:
                    self.mark_a_line_of_frameInfo()

            self.mutex.unlock()


class J3A_MetaData_RecvThd(BaseThread):
    meta_obj_list_ignal = pyqtSignal(list, list, list)
    meta_picinfo_signal = pyqtSignal(list)

    def __init__(self, _bOnLineRecvMode=True):
        super(J3A_MetaData_RecvThd, self).__init__(_bOnLineRecvMode)
        self.socket = zmq_sub_client_socket(ConfigConstantData.J3A_socket_if)

    def run(self) -> None:
        while True:
            self.mutex.lock()
            if self._isPause:
                self.cond.wait(self.mutex)
            print("J3 camera meta data recv thread is running")
            try:
                self.get_next_frame_info()

                if self.recv_message[0] == 8:  # meta data
                    self.Meta = protobuf_if.Meta(self.recv_message)
                    print("frame_id is:", self.Meta.frame_id)
                    self.meta_obj_list_ignal.emit(self.Meta.obj2Dbox_list, self.Meta.obj3Dbox_list, self.Meta.lane_list)
                    self.log_this_frame = True
                    if self.bOnLineRecvMode == False:
                        self.pause()

                # elif self.recv_message[0] == 0:  # h265 info
                # 	pass
                # print("1th long message len of %d"%msg_len)
                # elif self.recv_message[1] == 216:  # jpeg
                # 	self.meta_picinfo_signal.emit(self.recv_message)
                elif self.recv_message[0] == 255:
                    pass
                # if msg_len == 776:
                # 	print("3th long message len of 776")
                # else:
                # 	print("2th msg len of %d"%msg_len)

                if self.bLoggingFile and self.log_this_frame:
                    self.log_a_frame_to_file_as_a_line(self.recv_message)
                    if self.todo_mark:
                        self.mark_a_line_of_frameInfo()

            except Exception as e:
                print('J3A meta data recv error', e)

            self.mutex.unlock()


class ReadRadarLogFileThread(BaseThread):
    log_pcl_signal = pyqtSignal(dict)
    log_obj_signal = pyqtSignal(list)
    log_objInfo_signal = pyqtSignal(list)
    log_showPic_signal = pyqtSignal(str)

    def __init__(self, log_file_name):  # 区分视频文件还是hex
        super(ReadRadarLogFileThread, self).__init__(_bOnLineRecvMode=True)
        if log_file_name.endswith(".hex"):
            pass
        else:
            print('select a hex file, please!')
            return

        self.logFile = logFileMngt.RadarLogFileInfo(log_file_name)
        if self.logFile.hasPicFiles:
            self.log_showPic_signal.emit(self.logFile.getCurrPic())

        self.picShowInterval_s = 0.04  # 50ms
        self.timeStamp_s = 0
        self.finishDrawObj = False
        self.finishDrawPCL = False
        self.objctList = []
        self.currLineDataBytes = self.logFile.get_data_bytes(self.logFile.currLineNr)
        while len(self.currLineDataBytes) != ConfigConstantData.ObjListByteNr:
            self.logFile.next_line()
            self.currLineDataBytes = self.logFile.get_data_bytes(self.logFile.currLineNr)  # 第一行需要是objects

    def run(self) -> None:
        while True:
            self.mutex.lock()
            if self._isPause:
                self.cond.wait(self.mutex)

            # obj
            while len(self.currLineDataBytes) == ConfigConstantData.ObjListByteNr:
                objList = self.logFile.parse_obj_list(self.currLineDataBytes)
                presentationObj = objList.getPresentationInfo()
                self.logFile.next_line()
                self.currLineDataBytes = self.logFile.get_data_bytes(self.logFile.currLineNr)
            try:
                self.log_obj_signal.emit(presentationObj)
                self.log_objInfo_signal.emit(objList.ObjectList_Objects)
            except Exception as e:
                print(e)

            # pcl
            while len(self.currLineDataBytes) == ConfigConstantData.PclByteNr:
                plcList = self.logFile.parse_pcl(self.currLineDataBytes)
                # timeStamp_s = plcList.getTimeStamp_s()
                presentationPCL = plcList.getPresentationPcl()
                self.logFile.next_line()
                self.currLineDataBytes = self.logFile.get_data_bytes(self.logFile.currLineNr)
            self.log_pcl_signal.emit(presentationPCL.dict_hight2color)

            # pictures
            picName = self.logFile.getNextPic()
            # print('showing pic of', picName)
            self.log_showPic_signal.emit(picName)

            self.pause()
            self.mutex.unlock()
