# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03

import time
import struct
import cv2
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import QThread, pyqtSignal,QWaitCondition,QMutex,QDateTime
import os
import re
import presentationLayer
from mySocket import MyUdpSocket
import protocol
import procAsamMdf
# import CppApi
import logFileMngt
import ConfigConstantData

class BaseThread(QThread):
	def __init__(self, parent=None):
		super(BaseThread, self).__init__(parent)
		self.mutex = QMutex()
		self.cond = QWaitCondition()
		self._isPause = True

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
	def __init__(self):
		super(VideoRecordThread, self).__init__()
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
	def __init__(self):
		super(OriginalRadarThread, self).__init__()
		self.adapter_socket = MyUdpSocket()
		self.frmNr = 0
		self.mdf = procAsamMdf.MdfFile()
		self.timestamp = time.time()
		self.presentationPCL = presentationLayer.Pcl_Color()
		self.counter = 0
		self.radarLogFile = 0

	def draw_obj(self,data_bytes):
		self.counter +=1
		self.counter %= 20
		obj_buf = data_bytes[16:9385 + 16]
		obj_list = protocol.ARS548_ObjectList(obj_buf)
		objPresentations = obj_list.getPresentationInfo()

		if self.counter == 0: # reduce the frequency of data showing
			self.orgRadar_objInfo_signal.emit(obj_list.ObjectList_Objects[0:obj_list.ObjectList_NumOfObjects])
		else:
			self.orgRadar_obj_signal.emit(objPresentations)

	def draw_PCL(self, bytes_data):
		buf = bytes_data[16:35305 + 16]
		dList = protocol.ARS548_DetectionList(buf)
		self.presentationPCL = dList.getPresentationPcl()
		self.orgRadar_pcl_signal.emit(self.presentationPCL.dict_hight2color)

	def run(self) -> None:
		while True:
			self.mutex.lock()
			if self._isPause:
				self.cond.wait(self.mutex)
			print("OriginalRadarThread is running")
			try:
				recv_message, client = self.adapter_socket.udp_socket.recvfrom(self.adapter_socket.rcvBufLen)
				#test write log
				# if 50 == len(recv_message):
				# 	data = struct.unpack('>50B', recv_message)
				# 	print("data len 50",data)
				# elif 158 == len(recv_message):
				# 	data = struct.unpack('>158B', recv_message)
				# 	print("data len 158",data)
				# elif 803 == len(recv_message):
				# 	data = struct.unpack('>803B', recv_message)
				# 	print("data len 803",data)
				if ConfigConstantData.ObjListByteNr == len(recv_message): # objects
					strData = recv_message.hex(' ') +'\n'
					self.radarLogFile.write(strData)

					data = struct.unpack('>9401B', recv_message)
					bytes_data = int.from_bytes(data, byteorder='big').to_bytes(ConfigConstantData.ObjListByteNr, byteorder='big')
					self.draw_obj(bytes_data)

				elif ConfigConstantData.PclByteNr == len(recv_message): # pcl
					strData = recv_message.hex(' ') +'\n'
					self.radarLogFile.write(strData)

					data = struct.unpack('>35336B', recv_message)
					bytes_data = int.from_bytes(data, byteorder='big').to_bytes(ConfigConstantData.PclByteNr, byteorder='big')
					self.draw_PCL(bytes_data)


			except Exception as e:
				print(e)

			self.mutex.unlock()


class ReadRadarLogFileThread(BaseThread):
	log_pcl_signal = pyqtSignal(dict)
	log_obj_signal = pyqtSignal(list)
	log_objInfo_signal = pyqtSignal(list)
	log_showPic_signal = pyqtSignal(str)
	def __init__(self, log_file_name): #区分视频文件还是hex
		super(ReadRadarLogFileThread, self).__init__()
		if log_file_name.endswith(".hex"):
			pass
		else:
			print('select a hex file, please!')
			return



		self.logFile = logFileMngt.RadarLogFileInfo(log_file_name)
		if self.logFile.hasPicFiles:
			self.log_showPic_signal.emit(self.logFile.getCurrPic())

		self.picShowInterval_s = 0.04 # 50ms
		self.timeStamp_s = 0
		self.finishDrawObj = False
		self.finishDrawPCL = False
		self.objctList = []
		self.currLineDataBytes = self.logFile.get_data_bytes(self.logFile.currLineNr)
		while len(self.currLineDataBytes) != ConfigConstantData.ObjListByteNr:
			self.logFile.next_line()
			self.currLineDataBytes = self.logFile.get_data_bytes(self.logFile.currLineNr)# 第一行需要是objects


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
				timeStamp_s = plcList.getTimeStamp_s()
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






