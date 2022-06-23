__author__ = 'Yang HongXu'

import time
import struct
import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal,QWaitCondition,QMutex,QDateTime
import os.path

import presentationLayer
from mySocket import MyUdpSocket
import protocol
import procAsamMdf
# import CppApi
import logFileMngt

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

class TestThread(BaseThread):
	def run(self) -> None:
		print("TestThread start!!")
		while 1:
			print("TestThread is running")
	def __del__(self):
		print("TestThread is deleted")

	def quit(self) -> None:
		print("TestThread is quit")

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


class VideoPlayThread(BaseThread):

	def __init__(self):
		super(VideoPlayThread, self).__init__()
		self.cap = 0
		self.bPlaying = False
		self.newSize = (640, 480)
		self.ret = False
		self.frame = 0
		self.showImage = 0
		self.fps = int(30)
		self.frames = logFileMngt.getFrames()
		self.videoFileName = ""

	def run(self):
		# self.videoFileName = "log.mp4"
		# self.videoFileName = "video.mp4"
		self.cap = cv2.VideoCapture(self.videoFileName)
		self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
		self.ret, self.frame = self.cap.read()

		if self.cap.isOpened():
			self.bPlaying = True
		else:
			print("视频打开失败")

		while self.ret and self.isRunning():
			self.mutex.lock()
			if self._isPause:
				self.cond.wait(self.mutex)
			try:
				show = cv2.resize(self.frame, self.newSize)
				show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
				self.showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0],
											  QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
				print("VideoPlayThread is running!")
			except Exception as e:
				print(e)

			self.mutex.unlock()
			# 退出播放
			key = cv2.waitKey(int(1200/self.fps))  # 1000ms/fps
			self.ret, self.frame = self.cap.read()
			if key == 27:  # 按键esc
				break

		print("视频播放完成！")

	def quit(self):
		super(VideoPlayThread, self).quit()
		self.cap.release()
		cv2.destroyAllWindows()

def draw_obj(data_bytes):
	obj_buf = data_bytes[16:9385 + 16]
	obj_list = protocol.ARS548_ObjectList(obj_buf)
	objPresentations = []
	objNr = obj_list.ObjectList_NumOfObjects
	for j in range(objNr):
		objPresentations.append(obj_list.ObjectList_Objects[j].get_object_draw_info())
	return objPresentations , obj_list.ObjectList_Objects

def draw_PCL(bytes_data, pcl_color_map):
	buf = bytes_data[16:35305 + 16]
	dList = protocol.ARS548_DetectionList(buf)
	# dict from color to pos
	pcl_color_map.clear_dict()
	for i in range(dList.List_NumOfDetections):
		pcl_color_map.add_point_to_dict(dList.List_Detections[i].getPosn())
	return pcl_color_map


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

	def draw_obj(self,data_bytes):
		self.counter +=1
		self.counter %= 20
		obj_buf = data_bytes[16:9385 + 16]
		obj_list = protocol.ARS548_ObjectList(obj_buf)
		objPresentations = []
		objNr = obj_list.ObjectList_NumOfObjects
		for j in range(objNr):
			objPresentations.append(obj_list.ObjectList_Objects[j].get_object_draw_info())

		if self.counter == 0: # reduce the frequency of data showing
			self.orgRadar_objInfo_signal.emit(obj_list.ObjectList_Objects[0:obj_list.ObjectList_NumOfObjects])
		else:
			self.orgRadar_obj_signal.emit(objPresentations)



	def draw_PCL(self, bytes_data):
		buf = bytes_data[16:35305 + 16]
		dList = protocol.ARS548_DetectionList(buf)
		pos = []

		# dict from color to pos
		self.presentationPCL.clear_dict()

		colors = []
		# add road lane
		xs = []
		ys = []
		zs = []
		f_AzimuthAngle = []
		f_ElevationAngle = []
		f_Range = []
		rcs = []
		rel_speed = []



		for i in range(dList.List_NumOfDetections):
			self.presentationPCL.add_point_to_dict(dList.List_Detections[i].getPosn())
			x, y, z = dList.List_Detections[i].getPosn()
			xs.append(y)
			ys.append(x)
			zs.append(z)
			f_AzimuthAngle.append(dList.List_Detections[i].f_AzimuthAngle)
			f_ElevationAngle.append(dList.List_Detections[i].f_ElevationAngle)
			f_Range.append(dList.List_Detections[i].f_Range)
			rcs.append(dList.List_Detections[i].s_RCS)
			rel_speed.append(dList.List_Detections[i].f_RangeRate)

			posn = x, y, z
			pos.append(posn)



		# self.draw_pingbao_obj()
		self.orgRadar_pcl_signal.emit(self.presentationPCL.dict_hight2color)

	def run(self) -> None:
		while True:
			self.mutex.lock()
			if self._isPause:
				self.cond.wait(self.mutex)
			print("OriginalRadarThread is running")
			try:
				recv_message, client = self.adapter_socket.udp_socket.recvfrom(self.adapter_socket.rcvBufLen)
				# if 50 == len(recv_message):
				# 	data = struct.unpack('>50B', recv_message)
				# 	print("data len 50",data)
				# elif 158 == len(recv_message):
				# 	data = struct.unpack('>158B', recv_message)
				# 	print("data len 158",data)
				# elif 803 == len(recv_message):
				# 	data = struct.unpack('>803B', recv_message)
				# 	print("data len 803",data)
				if 9401 == len(recv_message): # objects
					data = struct.unpack('>9401B', recv_message)
					bytes_data = int.from_bytes(data, byteorder='big').to_bytes(9401, byteorder='big')
					self.draw_obj(bytes_data)
					# print("data len 9401", data)
				elif 35336 == len(recv_message): # pcl
					data = struct.unpack('>35336B', recv_message)
					bytes_data = int.from_bytes(data, byteorder='big').to_bytes(35336, byteorder='big')
					self.draw_PCL(bytes_data)
					# print("data len 35336", data)



				# bytes_data = int.from_bytes(data, byteorder='big').to_bytes(44, byteorder='big')
				# # add point
				# app_data = protocol.ARS548_Detection(bytes_data)
				# ptPosn = app_data.getPosn()
				# ptList = []
				# ptList.append(ptPosn)
				# self.pcl_posn_signal.emit(ptList)
				#
				# self.timestamp = time.time()
				# self.frmNr += 1
				# self.mdf.appendNewTimeStampData(app_data, self.timestamp)
			except Exception as e:
				print(e)



			# print(app_data)
			self.mutex.unlock()


class ReadRadarLogFileThread(BaseThread):
	log_pcl_signal = pyqtSignal(dict)
	log_obj_signal = pyqtSignal(list)
	road_lane_signal = pyqtSignal(list, list)
	update_progress_signal = pyqtSignal()
	log_objInfo_signal = pyqtSignal(list)
	def __init__(self, video_file_name): #区分视频文件还是hex
		super(ReadRadarLogFileThread, self).__init__()
		if video_file_name.endswith(".hex"):
			logFileName = video_file_name
		else:
			logFileName = logFileMngt.dict_video2radar[video_file_name]
		self.logFile = logFileMngt.RadarLogFileInfo(logFileName)


		self.finishDrawObj = False
		self.finishDrawPCL = False
		self.objctList = []
		self.presentationPCL = presentationLayer.Pcl_Color()

	def draw_PCL(self,bytes_data):
		buf = bytes_data[16:35305 + 16]
		dList = protocol.ARS548_DetectionList(buf)
		pos = []

		# dict from color to pos
		self.presentationPCL.clear_dict()

		colors = []
		xs = []
		ys = []
		zs = []
		f_AzimuthAngle = []
		f_ElevationAngle = []
		f_Range = []
		rcs = []
		rel_speed = []



		for i in range(dList.List_NumOfDetections):
			self.presentationPCL.add_point_to_dict(dList.List_Detections[i].getPosn())
			x, y, z = dList.List_Detections[i].getPosn()
			xs.append(y)
			ys.append(x)
			zs.append(z)
			f_AzimuthAngle.append(dList.List_Detections[i].f_AzimuthAngle)
			f_ElevationAngle.append(dList.List_Detections[i].f_ElevationAngle)
			f_Range.append(dList.List_Detections[i].f_Range)
			rcs.append(dList.List_Detections[i].s_RCS)
			rel_speed.append(dList.List_Detections[i].f_RangeRate)

			posn = x, y, z
			pos.append(posn)
		self.log_pcl_signal.emit(self.presentationPCL.dict_hight2color)

	def draw_obj(self,data_bytes):
		obj_buf = data_bytes[16:9385 + 16]
		obj_list = protocol.ARS548_ObjectList(obj_buf)
		objPresentations = []
		for j in range(obj_list.ObjectList_NumOfObjects):
			objPresentations.append(obj_list.ObjectList_Objects[j].get_object_draw_info())
		self.log_obj_signal.emit(objPresentations)

	def draw_pingbao_obj(self):
		objPresentations = []
		for obj in self.objctList.object_list:
			objPresentations.append(presentationLayer.MyCuboid(length=obj.length, width=obj.width,
															   x=obj.x, y=obj.y,z=obj.z, _type=obj.typ, _id=obj.id,
																_absV_x=obj.length, _absV_y=obj.width,_stMovement=obj.movement_state))


		self.log_obj_signal.emit(objPresentations)

	def update_progress(self):
		self.update_progress_signal.emit()

	def run(self) -> None:
		while True:
			self.mutex.lock()
			if self._isPause:
				self.cond.wait(self.mutex)

			pcl_dataBytes, obj_dataBytes = self.logFile.get_data_bytes()
			# self.draw_PCL(pcl_dataBytes)
			pclList = draw_PCL(pcl_dataBytes, self.presentationPCL)
			self.log_pcl_signal.emit(pclList.dict_hight2color)

			drawBoxList, objList = draw_obj(obj_dataBytes)
			self.log_obj_signal.emit(drawBoxList)
			self.log_objInfo_signal.emit(objList)


			print("LogFileReadThread is running")
			self.pause()
			self.update_progress()
			self.mutex.unlock()






