# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
import sys
import os.path
import re
import queue as Queue
import bisect as bs
import my_util
import hex_log_file
import presentationLayer
import testMainWindow_Ui
import time
import mySocket
import protocol
from PyQt5.QtCore import QThread, pyqtSignal,QTimer,QDateTime
from PyQt5 import QtCore,QtGui
import pyqtgraph.opengl as gl
import pyqtgraph
import numpy as np
import cv2
import threadMngt
# from PyQt5.QtMultimedia import (QCameraInfo,QCameraImageCapture,
#       QImageEncoderSettings,QMultimedia,QVideoFrame,QSound,QCamera)

from PyQt5.QtCore import  pyqtSlot,QUrl,QDir, QFileInfo,Qt,QEvent
# from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer

import ConfigConstantData


map_hight_color = {1:(0.,0,1,1),
                   2:(0,1,1,1),
                   3:(0,1,0,1),
                   4:(1,1,0,1),
                   5:(1,0,0,1)}
class MyController(QMainWindow, testMainWindow_Ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyController, self).__init__()

        self.setupUi(self)
        self.testCntr = 0

        # 快进
        self.right_button.clicked.connect(self.up_time)
        # 快退
        self.left_button.clicked.connect(self.down_time)
        # 下拉选项
        self.cb.currentIndexChanged.connect(self.RunModeChange)
        # 进度条
        self.timeSlider.valueChanged.connect(self.on_timeslider_valueChanged)
        self.timeSlider.sliderReleased.connect(self.on_timeslider_valueChanged)

        #模式初始化
        self.set_default_mode()


        # 变量初始化
        self.picNameNr = int(0)
        self.total_time_s = 0
        self.readRadarLogFileThread = None



        self.camera = cv2.VideoCapture(ConfigConstantData.camera_id,cv2.CAP_DSHOW)  # QCamera对象4/
        testFrame = self.camera.retrieve()
        self.camera_valid =  testFrame[0]
        if self.camera_valid == False:
            print('no usb camera plug in !')


        self.orgRadarThread = threadMngt.OriginalRadarThread()


        if ConfigConstantData.MachineType == ConfigConstantData.J3System:
            self.timestamp_map_pic={}
            self.timestamp_map_pic_key_list = []

            self.orgRadarThread.Radar2D_obj_signal.connect(self.radar408_2dBox_show)
            self.orgRadarThread.fused_objList_signal.connect(self.fused_obj_list_show)
            self.orgRadarThread.start()
            self.orgRadarThread.resume()

            self.metaThread = threadMngt.J3A_MetaData_RecvThd()
            self.metaThread.meta_obj_list_ignal.connect(self.show_meta_objects)
            # self.metaThread.meta_picinfo_signal.connect(self.buf_pic_info)
            self.metaThread.start()
            self.metaThread.resume()

            # new added
            self.h265Thread = threadMngt.H265_PicRecvThd()
            self.h265Thread.cv2_pic_recv_signal.connect(self.buf_pic_info)
            self.h265Thread.start()
            self.h265Thread.resume()
            self.curr_pic = None

            self.timer_sensor_show = QtCore.QTimer()  # 控制雷达的刷新频率
            self.timer_sensor_show.timeout.connect(self.multi_pic_show)
            self.timer_sensor_show.start(ConfigConstantData.timer_online_sensor_show_ms)

            self.log_read_timer = QtCore.QTimer()  # 控制雷达的刷新频率
            self.log_read_timer.timeout.connect(self.resume_Threads_OffLine)

            # self.timer_pic_show = QtCore.QTimer()  # 控制图片的刷新频率
            # self.timer_pic_show.timeout.connect(self.showCamera)
            # self.timer_pic_show.start(ConfigConstantData.timer_online_pic_show_ms)

            self.pic_shape = (ConfigConstantData.pic_height, ConfigConstantData.pic_width,3)
            self.pic_org = np.zeros(self.pic_shape, dtype=np.uint8)
            self.pic_meta = np.zeros(self.pic_shape, dtype=np.uint8)
            self.pic_fusion = np.zeros(self.pic_shape, dtype=np.uint8)
            self.currOffLinePic = None

            self.btnMarkRecord.clicked.connect(self.set_mark_flag)

            self.checkBox_pic.stateChanged.connect(self.set_multi_pic_weight)
            self.checkBox_OrgObj.stateChanged.connect(self.set_multi_pic_weight)
            self.checkBox_Fusion.stateChanged.connect(self.set_multi_pic_weight)

            self.weight_pic_org = 1
            self.weight_pic_fusion = 1
            self.weight_pic_meta = 1

            self.meta_2d_obj_list = []
            self.meta_3d_obj_list = []
            self.meta_lane_list = []
            # self.meta_pic_queue = Queue(5)

            self.radar_2dBox_list = []
            self.fusion_2dBox_list = []
            self.fusion_3dBox_list= []

            self.combox_marked_points.currentIndexChanged.connect(self.jump_to_marked_point)

        elif ConfigConstantData.MachineType == ConfigConstantData.radar4D_548:
            # table
            self.model = QtGui.QStandardItemModel(15, 15)
            self.model.setVerticalHeaderLabels(['u_ID',
                                                'u_Position_X',
                                                'u_Position_Y',
                                                'u_Position_Z',
                                                'u_Existence_Probability',
                                                'u_Classification_Car',
                                                'u_Classification_Truck',
                                                'u_Classification_Motorcycle',
                                                'u_Classification_Bicycle',
                                                'u_Classification_Pedestrian',
                                                'u_Classification_Animal',
                                                'u_Classification_Hazard',
                                                'u_Classification_Unknown',
                                                'u_Shape_Length_Edge_Mean',
                                                'u_Shape_Width_Edge_Mean'])
            self.tableView.setModel(self.model)

            self.radar_timer_step = ConfigConstantData.timer_readlogfile_ms
            self.timer_radar = QtCore.QTimer()  # 控制雷达的刷新频率
            self.timer_radar.timeout.connect(self.resume_logThread)
            self.timer_radar.start(self.radar_timer_step)


            self.orgRadarThread.orgRadar_pcl_signal.connect(self.show_pcl)  # 仿真文件数据
            self.orgRadarThread.orgRadar_obj_signal.connect(self.show_objects)  # 仿真文件数据
            self.orgRadarThread.orgRadar_objInfo_signal.connect(self.show_objectsInfo)  # 表格控件
            self.orgRadarThread.start()

    def set_mark_flag(self):
        self.metaThread.todo_mark = True

    def jump_to_marked_point(self):
        curr_idx = self.combox_marked_points.currentIndex()
        if curr_idx == 0:
            return
        str_timestamp = self.combox_marked_points.itemText(curr_idx)
        timestamp = my_util.get_timestamp_from_str(str_timestamp)
        self.metaThread.log_file.jump_to_timestamp(timestamp)

    def resume_pic_show(self):
        i = bs.bisect_left(self.timestamp_map_pic_key_list, self.metaThread.log_file.get_curr_timestamp())
        pic_key = self.timestamp_map_pic_key_list[i]

        self.currOffLinePic = QtGui.QPixmap(self.timestamp_map_pic[pic_key]).scaled(640, 480)
        self.ref_pic_lable.setPixmap(self.currOffLinePic)

    def resume_Threads_OffLine(self):
        if self.isRunning:
            if self.metaThread.isRunning():
                self.metaThread.resume()
                self.update_log_progress()
            if self.orgRadarThread.isRunning():
                self.orgRadarThread.resume1(self.metaThread.log_file.get_curr_timestamp())

            self.resume_pic_show()

    def pic_show(self):
        pass
        # if self.checkBox_pic.isChecked():
        #     pic_info = self.meta_pic_queue.get()
        #     img = cv2.imdecode(np.frombuffer(pic_info, np.uint8), cv2.IMREAD_COLOR)
        #     data = cv2.resize(img, dsize=(ConfigConstantData.pic_width, ConfigConstantData.pic_height), fx=1, fy=1, interpolation=cv2.INTER_LINEAR)

    def buf_pic_info(self):
        self.curr_pic = self.h265Thread.recv_message

    def radar408_2dBox_show(self, radar_2dBox_list):
        self.radar_2dBox_list = []
        self.radar_2dBox_list = radar_2dBox_list

    def fused_obj_list_show(self, fused_2d_list,fused_3d_list):
        self.fusion_2dBox_list = []
        self.fusion_3dBox_list = []
        self.fusion_2dBox_list = fused_2d_list
        self.fusion_3dBox_list = fused_3d_list

    def clear_pic(self):
        return np.zeros(self.pic_shape, dtype=np.uint8)

    def set_multi_pic_weight(self):
        if self.checkBox_pic.isChecked():
            self.weight_pic_org = 1
        else:
            self.weight_pic_org = 0

        if self.checkBox_OrgObj.isChecked():
            self.weight_pic_meta = 1
        else:
            self.weight_pic_meta = 0

        if self.checkBox_Fusion.isChecked():
            self.weight_pic_fusion = 1
        else:
            self.weight_pic_fusion = 0

    def set_org_pic(self):
        if self.checkBox_pic.isChecked():
            if self.isOnlineMode:
                if self.curr_pic is not None:
                    nparr = np.asarray(bytearray(self.curr_pic), dtype="uint8")
                    self.pic_org = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            else:
                if self.isRunning:
                    try:
                        self.ref_pic_lable.setPixmap(self.currOffLinePic)
                    except Exception as e:
                        print(e)


    def set_meta_pic(self):
        self.pic_meta = self.clear_pic()
        if self.checkBox_OrgObj.isChecked():
            for box_2d in self.meta_2d_obj_list:
                box_2d.draw_to_pic(self.pic_meta)

            for box_3d in self.meta_3d_obj_list:
                box_3d.draw_to_pic(self.pic_meta)

            for lane in self.meta_lane_list:
                lane.draw_to_pic(self.pic_meta)


    def set_fusion_pic(self):

        self.pic_fusion = self.clear_pic()
        if self.checkBox_Fusion.isChecked():
            for box_2d in self.fusion_2dBox_list:
                box_2d.draw_to_pic(self.pic_fusion)
            for box_3d in self.fusion_3dBox_list:
                box_3d.draw_to_pic(self.pic_fusion)
            for box_2d_ in self.radar_2dBox_list:
                box_2d_.draw_to_pic(self.pic_fusion)

    def clear_lable(self):#清除图片上的目标物信息
        pass
        # if self.curr_pic is not None:
        #     pic = np.asarray(bytearray(self.curr_pic), dtype="uint8")
        #     print("curr pic is not none len is ", len(self.curr_pic))
        # else:
        #     print("pic is none")
        #     pic = np.zeros(self.pic_shape, dtype=np.uint8)
        # # pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        # img_decode = cv2.imdecode(pic, cv2.IMREAD_COLOR)
        #
        # pic = QtGui.QImage(img_decode.data, img_decode.shape[1], img_decode.shape[0], QImage.Format_RGB888)
        # self.lable_main.setPixmap(QtGui.QPixmap.fromImage(pic).scaled(1240, 720, QtCore.Qt.KeepAspectRatio))
        # self.lable_main.setPixmap(QtGui.QPixmap.fromImage(pic))

    def multi_pic_show(self):
        self.set_org_pic()
        self.set_meta_pic()
        self.set_fusion_pic()

        self.clear_lable()

        #叠加图片
        pic  = cv2.addWeighted(self.pic_meta, self.weight_pic_meta, self.pic_fusion, self.weight_pic_fusion, 0)
        pic1  = cv2.addWeighted(pic, 1, self.pic_org, self.weight_pic_org, 0)

        pic2 = cv2.cvtColor(pic1, cv2.COLOR_BGR2RGB)
        pic3 = QtGui.QImage(pic2.data, pic2.shape[1], pic2.shape[0],QImage.Format_RGB888)
        self.lable_main.setPixmap(QtGui.QPixmap.fromImage(pic3))

    def show_meta_objects(self,box_2d_list,box_3d_list, lane_list):
        self.meta_2d_obj_list = []
        self.meta_3d_obj_list = []
        self.meta_lane_list = []
        self.pic_meta = self.clear_pic()

        if self.checkBox_OrgObj.isChecked():
            self.meta_2d_obj_list = box_2d_list
            self.meta_3d_obj_list = box_3d_list
            self.meta_lane_list = lane_list

    def update_log_progress(self):
        self.timeSlider.setValue(self.metaThread.log_file.get_progress())

        ts_curr = self.metaThread.log_file.get_curr_timestamp()

        timeStamp_start = self.metaThread.log_file.timestamp_list[0]

        delta_t = ts_curr - timeStamp_start

        currTime_str = my_util.strfdelta(delta_t, "%H:%M:%S")

        self.LabRatio.setText(currTime_str)

    def init_timeSlider(self):
        major_log_file_handl = self.metaThread.log_file

        timeStamp_start = major_log_file_handl.timestamp_list[0]
        timeStamp_end = major_log_file_handl.timestamp_list[major_log_file_handl.log_file_size-1]

        self.total_time_s = timeStamp_end - timeStamp_start

        totalTime_str = my_util.strfdelta(self.total_time_s, "%H:%M:%S")


        self.LabRatio.setText('00:00:00')
        self.LabTotal.setText('/ '+totalTime_str)
        self.timeSlider.setMaximum(major_log_file_handl.log_file_size)
        self.timeSlider_oldValue = 0

    def on_timeslider_valueChanged(self):
        if abs(self.timeSlider.value() - self.timeSlider_oldValue) > 10:
            newLogFileLineNr =int(self.metaThread.log_file.log_file_size * self.timeSlider.value()/self.timeSlider.maximum())
            self.metaThread.log_file.set_progress(newLogFileLineNr)

            if not self.isRunning:
                self.metaThread.resume()

        self.timeSlider_oldValue = self.timeSlider.value()

    def set_default_mode(self):
        self.isRunning = False
        self.isOnlineMode = True
        self.btnPlay.setDisabled(False)
        self.btnMarkRecord.setDisabled(True)
        self.left_button.setDisabled(True)
        self.right_button.setDisabled(True)
        self.timeSlider.setDisabled(True)
        self.cb.setDisabled(False)
        self.btnOpen.setDisabled(True)

    def show_pcl(self, dict):
        self.GLView_OrgRadar.removePoints()
        for key in dict.keys():
            if dict[key]:
                self.GLView_OrgRadar.addPoints(pos=dict[key], size=1, color=map_hight_color[key])
        self.GLView_OrgRadar.addPointsDict()

    def show_objectsInfo(self, objList):
        for i in range(len(objList)):
            row = 0
            self.tableItem(row, i, objList[i].u_ID)
            row+=1
            self.tableItem(row,i,objList[i].u_Position_X)
            row+=1
            self.tableItem(row,i,objList[i].u_Position_Y)
            row += 1
            self.tableItem(row, i, objList[i].u_Position_Z)
            row+=1
            self.tableItem(row,i,objList[i].u_Existence_Probability)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Car)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Truck)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Motorcycle)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Bicycle)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Pedestrian)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Animal)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Hazard)
            row+=1
            self.tableItem(row, i, objList[i].u_Classification_Unknown)
            row+=1
            self.tableItem(row, i, objList[i].u_Shape_Length_Edge_Mean)
            row += 1
            self.tableItem(row, i, objList[i].u_Shape_Width_Edge_Mean)

    def show_objects(self, objPre):
        self.GLView_FuseRadar.clear3Dbox()
        for i in range(len(objPre)):
            size = QtGui.QVector3D(objPre[i].width,objPre[i].length, objPre[i].height)
            # if objPre[i].stMovement:
            #     color = QtGui.QColor(0, 255, 0)
            # else:
            #     color = QtGui.QColor(255, 0, 0)
            self.GLView_FuseRadar.add3Dbox(pos=objPre[i].posn, size=size, color=objPre[i].color, _id=objPre[i].id,colorType=objPre[i].type)

    def tableItem(self, row, col, val):
        item = QtGui.QStandardItem()
        self.model.setItem(row, col, item)
        index = self.model.index(row, col)
        value = QtCore.QVariant(val)
        self.model.setData(index, value)

    def resume_logThread(self):# 需要修改，在线接收时，不适用计时器恢复线程！！！！！！！！！！！！！！！
        if not self.isOnlineMode and self.isRunning:
            self.update_log_progress()
            self.readRadarLogFileThread.resume()

        if self.isOnlineMode:
            frame = self.showCamera()

    def getCurrTimeStr(self):
        timestamp = time.time()
        strTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(timestamp))
        return strTime

    def savePictures(self, f):
        ts = my_util.get_timestamp_str()
        filStr = self.log_folder_path[-26:-8] + ts+'.jpg'
        picName =self.log_folder_path + '/' + filStr
        self.picNameNr += 1
        res = cv2.resize(f, (320,240), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(picName, res)

    def showCamera(self):
        if self.self.camera_valid:
            r, f = self.camera.read()
            if r:
                show_image = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
                show_image = QtGui.QImage(show_image.data, show_image.shape[1], show_image.shape[0], QImage.Format_RGB888)
                self.ref_pic_lable.setPixmap(QtGui.QPixmap.fromImage(show_image).scaled(640, 480, QtCore.Qt.KeepAspectRatio))
                if self.isRunning:
                    self.savePictures(f)
            return f

    def set_runtime_mode(self):

        self.btnOpen.setDisabled(True)
        self.left_button.setDisabled(True)
        self.right_button.setDisabled(True)
        self.btnMarkRecord.setDisabled(True)

        self.btnPlay.setDisabled(False)
        self.btnPlay.setIcon(self.iconPlay)
        self.timeSlider.setDisabled(True)
        self.stackedWidget.setCurrentIndex(0)

        self.isOnlineMode = True

    def set_simulink_logfile_mode(self):
        self.btnPlay.setDisabled(True)
        self.timeSlider.setDisabled(False)
        self.btnOpen.setDisabled(False)
        self.stackedWidget.setCurrentIndex(1)
        self.isOnlineMode = False

    def RunModeChange(self, index):
        if index == 0:  # log文件读取
            self.set_simulink_logfile_mode()
        else:  # 实时数据采集
            self.set_runtime_mode()


        self.reset_threads(self.isOnlineMode)

    # 快进
    def up_time(self):
        self.metaThread.log_file.next_frame()
        self.metaThread.resume()
        self.orgRadarThread.resume1(self.metaThread.log_file.get_curr_timestamp())
        self.resume_pic_show()

    def down_time(self):
        self.metaThread.log_file.goback_oneStep()
        self.metaThread.resume()
        self.orgRadarThread.resume1(self.metaThread.log_file.get_curr_timestamp())
        self.resume_pic_show()

    def getPicMap_with_suffix(self,path, suffix):
        # input_template_All = []
        map_pic = {}
        ts_list=[]
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if os.path.splitext(name)[1] == suffix:
                    print(name)
                    pic_full_name = os.path.join(root, name)
                    str_ts = name[-16:-4]
                    ts = my_util.get_timestamp_from_str(str_ts)
                    ts_list.append(ts)
                    map_pic[ts] = pic_full_name

        return map_pic,ts_list

    def getFileList_with_suffix(self,path, suffix):

        input_template_All_Path = []
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                if os.path.splitext(name)[1] == suffix:
                    print(name)
                    input_template_All_Path.append(os.path.join(root, name))

        return input_template_All_Path

    def reset_threads(self,bOnLineMode=True):
        self.metaThread.quit()
        self.orgRadarThread.quit()

        self.orgRadarThread = threadMngt.OriginalRadarThread(False)
        self.orgRadarThread.Radar2D_obj_signal.connect(self.radar408_2dBox_show)
        self.orgRadarThread.fused_objList_signal.connect(self.fused_obj_list_show)
        self.orgRadarThread.start()


        self.metaThread = threadMngt.J3A_MetaData_RecvThd(False)
        self.metaThread.meta_obj_list_ignal.connect(self.show_meta_objects)
        # self.metaThread.meta_picinfo_signal.connect(self.buf_pic_info)
        self.metaThread.start()


    def init_mark_points_comb(self):
        if len(self.metaThread.log_file.marked_timestamp_list)>0:
            self.combox_marked_points.clear()
            self.combox_marked_points.addItem('marked_points!')
            self.combox_marked_points.addItems(self.metaThread.log_file.marked_timestamp_list)
            self.combox_marked_points.setCurrentIndex(0)
        else:
            self.combox_marked_points.setDisabled(True)



    @pyqtSlot()  ##打开文件
    def on_btnOpen_clicked(self):
        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "选择视频文件"
        # filt = "视频文件(*.wmv *.avi *.mp4);;所有文件(*.*)"
        filt = "log file(*.hex);;所有文件(*.*)"

        # fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        folde_path = QFileDialog.getExistingDirectory()

        self.reset_threads(True)

        hex_list = self.getFileList_with_suffix(folde_path, '.hex')
        self.timestamp_map_pic, self.timestamp_map_pic_key_list = self.getPicMap_with_suffix(folde_path, '.jpg')

        for hexFile in hex_list:
            if hexFile.endswith(ConfigConstantData.logfile_tail_affix_J3Camera):
                self.metaThread.log_file = hex_log_file.Parse_Majority_Log_File(hexFile)
            elif hexFile.endswith(ConfigConstantData.logfile_tail_affix_J3Fusion):
                self.orgRadarThread.log_file = hex_log_file.Parse_Extra_Log_File(hexFile)

        if self.metaThread.log_file.log_file_size == 0:
            print('no meta data log info!')
            return

        self.init_mark_points_comb()

        self.isRunning = True
        self.btnPlay.setDisabled(False)

        self.btnOpen.setDisabled(True)
        self.btnPlay.setIcon(self.iconPause)

        self.init_timeSlider()

        self.log_read_timer.start(self.metaThread.log_file.delta_t_ms)

    def show_one_pic(self, picFullPath):
        # image = QtGui.QPixmap(picFullPath).scaled(320, 320)
        image = QtGui.QPixmap(picFullPath).scaled(320, 240)
        # 显示图片
        self.lable_camera.setPixmap(image)

    def creat_new_log_folde(self):
        curPath = os.path.dirname(os.path.realpath(sys.argv[0]))  # 获取系统当前目录
        sharedName = ConfigConstantData.logFile_head_affix + self.getCurrTimeStr()
        self.log_folder_path = curPath + ConfigConstantData.picture_saved_path + sharedName
        print('log folder path:', self.log_folder_path)
        os.makedirs(self.log_folder_path)
        if ConfigConstantData.MachineType == ConfigConstantData.J3System:
            self.metaThread.log_file = open(self.log_folder_path + "/" + sharedName + ConfigConstantData.logfile_tail_affix_J3Camera, 'a')
            self.orgRadarThread.log_file = open(self.log_folder_path + "/" + sharedName + ConfigConstantData.logfile_tail_affix_J3Fusion, 'a')
            self.metaThread.bLoggingFile  = True
        elif ConfigConstantData.MachineType == ConfigConstantData.radar4D_548:
            self.orgRadarThread.log_file = open(self.log_folder_path + "/" + sharedName + ConfigConstantData.logfile_tail_affix_4D548, 'a')
        self.orgRadarThread.bLoggingFile = True

    @pyqtSlot()  ##播放
    def on_btnPlay_clicked(self):
        if self.isOnlineMode:  # 实时数据采集
            if self.isRunning:  # 如果正在运行，则暂停，并保存文件
                self.btnPlay.setIcon(self.iconPlay)
                self.btnMarkRecord.setDisabled(True)
                if self.orgRadarThread.bLoggingFile:
                    self.orgRadarThread.bLoggingFile = False
                    self.orgRadarThread.log_file.close()
                if ConfigConstantData.MachineType == ConfigConstantData.J3System:
                    if self.metaThread.bLoggingFile:
                        self.metaThread.bLoggingFile = False
                        self.metaThread.log_file.close()
                self.timer_sensor_show.start(ConfigConstantData.timer_online_sensor_show_ms)
            else:  # 如果没有运行，则开始记录
                self.creat_new_log_folde()
                self.btnPlay.setIcon(self.iconPause)
                # when write log file,slow down the timer to show sensor data
                self.btnMarkRecord.setDisabled(False)
                self.timer_sensor_show.start(ConfigConstantData.timer_online_sensor_show_and_log_ms)

        else:  # log文件读取
            if self.isRunning:
                self.metaThread.pause()
                self.orgRadarThread.pause()
                self.left_button.setDisabled(False)
                self.right_button.setDisabled(False)
                self.btnOpen.setDisabled(False)
                self.btnPlay.setIcon(self.iconPlay)
            else:
                self.metaThread.resume()
                self.orgRadarThread.resume()
                self.right_button.setDisabled(True)
                self.left_button.setDisabled(True)
                self.btnOpen.setDisabled(True)
                self.btnPlay.setIcon(self.iconPause)

        self.isRunning = not self.isRunning

    @pyqtSlot()
    def btn_onOff_ckick(self):
        self.bOnLine = not self.bOnLine
        self.button_mod_select.setDisabled(self.bOnLine)

        if self.bOnLine:
            self.button_run_stop.setText("OffLine")
            if self.bSimulink:
                self.readRadarLogFileThread.resume()
                self.replayThread.resume()
            else:
                self.orgRadarThread.resume()
                self.cameraThread.resume()
        else:
            self.button_run_stop.setText("OnLine")
            if self.bSimulink:
                self.readRadarLogFileThread.pause()
                self.replayThread.pause()
            else:
                self.orgRadarThread.pause()
                self.cameraThread.pause()
                self.saveRadarInfo()

    def addPoints(self):
        self.GLView_FuseRadar.addPoints(pos=[(5, 5, 1), (3, 4, 1)], size=0.1,
                                      color=(1.0, 0.0, 0.0, 1))  # 当w使用addItem()后，才会生效显示图像

    def clearPoints(self):
        md.GLView_FuseRadar.removePoints()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    md = MyController()
    md.showMaximized()
    md.show()

    sys.exit(app.exec_())
