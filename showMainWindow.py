# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
import sys
import os.path

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
from PyQt5.QtMultimedia import (QCameraInfo,QCameraImageCapture,
      QImageEncoderSettings,QMultimedia,QVideoFrame,QSound,QCamera)

from PyQt5.QtCore import  pyqtSlot,QUrl,QDir, QFileInfo,Qt,QEvent
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer

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

        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # QCamera对象
        self.orgRadarThread = threadMngt.OriginalRadarThread()

        if ConfigConstantData.MachineType == ConfigConstantData.J3System:
            self.orgRadarThread.Radar2D_obj_signal.connect(self.radar408_2dBox_show)
            self.orgRadarThread.fused_objList_signal.connect(self.fused_obj_list_show)
            self.orgRadarThread.start()
            self.orgRadarThread.resume()

            self.metaThread = threadMngt.J3A_MetaData_RecvThd()
            self.metaThread.meta_obj_list_ignal.connect(self.show_meta_objects)
            self.metaThread.start()
            self.metaThread.resume()

            self.timer_sensor_show = QtCore.QTimer()  # 控制雷达的刷新频率
            self.timer_sensor_show.timeout.connect(self.multi_pic_show)
            self.timer_sensor_show.start(ConfigConstantData.timer_online_sensor_show_ms)

            self.pic_shape = (ConfigConstantData.pic_height, ConfigConstantData.pic_width,3)
            self.pic_org = np.zeros(self.pic_shape, dtype=np.uint8)
            self.pic_meta = np.zeros(self.pic_shape, dtype=np.uint8)
            self.pic_fusion = np.zeros(self.pic_shape, dtype=np.uint8)



            self.checkBox_pic.stateChanged.connect(self.set_multi_pic_weight)
            self.checkBox_OrgObj.stateChanged.connect(self.set_multi_pic_weight)
            self.checkBox_Fusion.stateChanged.connect(self.set_multi_pic_weight)

            self.weight_pic_org = 1
            self.weight_pic_fusion = 1
            self.weight_pic_meta = 1

            self.meta_2d_obj_list = []
            self.meta_3d_obj_list = []

            self.radar_2dBox_list = []
            self.fusion_2dBox_list = []
            self.fusion_3dBox_list= []

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
        self.pic_org = self.clear_pic()
        if self.checkBox_pic.isChecked():
            r, f = self.camera.read()
            if r:
                self.pic_org = cv2.resize(f, (ConfigConstantData.pic_width, ConfigConstantData.pic_height))

    def set_meta_pic(self):
        self.pic_meta = self.clear_pic()
        if self.checkBox_OrgObj.isChecked():
            for box_2d in self.meta_2d_obj_list:
                box_2d.draw_to_pic(self.pic_meta)

            for box_3d in self.meta_3d_obj_list:
                box_3d.draw_to_pic(self.pic_meta)

            # test code
            # box = presentationLayer.Box_2D(100.123,20.456,30.789,40.111)
            # box.set_color(presentationLayer.My_cv2_Color.Red)
            # box.set_text("hello")
            # box.draw_to_pic(self.pic_meta)
            #
            # pis=[(80,400),(180,400),(200,300),(100,300),(80,600),(180,600),(200,500),(100,500)]
            # box_3D = presentationLayer.Box_3D(pis)
            # box_3D.set_color(presentationLayer.My_cv2_Color.Red)
            # box_3D.set_text("hello 3D  box")
            # box_3D.draw_to_pic(self.pic_meta)

    def set_fusion_pic(self):
        self.pic_fusion = self.clear_pic()
        if self.checkBox_Fusion.isChecked():
            for box_2d in self.fusion_2dBox_list:
                box_2d.draw_to_pic(self.pic_fusion)
            for box_3d in self.fusion_3dBox_list:
                box_3d.draw_to_pic(self.pic_fusion)
            for box_2d in self.radar_2dBox_list:
                box_2d.draw_to_pic(self.pic_fusion)

            # box = presentationLayer.Box_2D(100,2000,30,40)
            # box.set_color(presentationLayer.My_cv2_Color.Green)
            # box.set_text("fusion")
            # box.draw_to_pic(self.pic_fusion)

    def clear_lable(self):
        pic = np.zeros(self.pic_shape, dtype=np.uint8)
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        pic = QtGui.QImage(pic.data, pic.shape[1], pic.shape[0], QImage.Format_RGB888)
        self.lable_main.setPixmap(QtGui.QPixmap.fromImage(pic))

    def multi_pic_show(self):
        self.set_org_pic()
        self.set_meta_pic()
        self.set_fusion_pic()

        self.clear_lable()

        pic = cv2.addWeighted(self.pic_org, self.weight_pic_org, self.pic_meta, self.weight_pic_meta, 0)
        pic = cv2.addWeighted(pic, 1, self.pic_fusion, self.weight_pic_fusion,  0)

        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        pic = QtGui.QImage(pic.data, pic.shape[1], pic.shape[0],QImage.Format_RGB888)
        self.lable_main.setPixmap(QtGui.QPixmap.fromImage(pic))

    def show_meta_objects(self,box_2d_list,box_3d_list):
        self.meta_2d_obj_list = []
        self.meta_3d_obj_list = []
        self.pic_meta = self.clear_pic()

        if self.checkBox_OrgObj.isChecked():
            self.meta_2d_obj_list = box_2d_list
            self.meta_3d_obj_list = box_3d_list

    def update_log_progress(self):
        self.timeSlider.setValue(self.readRadarLogFileThread.logFile.currLineNr)
        currTime_s =self.total_time_s * self.timeSlider.value()/self.timeSlider.maximum()
        currTime_str =time.strftime("%H:%M:%S", time.gmtime(currTime_s))

        self.LabRatio.setText(currTime_str)

    def init_timeSlider(self):
        timeStamp_start = self.readRadarLogFileThread.logFile.getTimeStampByLineNr(0)
        lastLineNr  = self.readRadarLogFileThread.logFile.log_file_size-1
        timeStamp_end = self.readRadarLogFileThread.logFile.getTimeStampByLineNr(lastLineNr)

        self.total_time_s = timeStamp_end - timeStamp_start

        totalTime_str =time.strftime("%H:%M:%S", time.gmtime(self.total_time_s))

        self.LabRatio.setText('00:00:00')
        self.LabTotal.setText('/ '+totalTime_str)
        self.timeSlider.setMaximum(self.readRadarLogFileThread.logFile.log_file_size)
        self.timeSlider_oldValue = 0

    def on_timeslider_valueChanged(self):
        if abs(self.timeSlider.value() - self.timeSlider_oldValue) > 10:
            newLogFileLineNr =int(self.readRadarLogFileThread.logFile.log_file_size * self.timeSlider.value()/self.timeSlider.maximum())
            self.readRadarLogFileThread.logFile.set_Progress(newLogFileLineNr)

            if not self.isRunning:
                self.readRadarLogFileThread.resume()

        self.timeSlider_oldValue = self.timeSlider.value()

    def set_default_mode(self):
        self.isRunning = False
        self.isOnlineMode = True
        self.btnPlay.setDisabled(False)
        # self.btnStop.setDisabled(True)
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
            if self.isRunning:
                self.savePictures(frame)

    def getCurrTimeStr(self):
        timestamp = time.time()
        strTime = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(timestamp))
        return strTime

    def savePictures(self, f):
        filStr = self.log_folder_path[-26:] + '_Frame_' + str(self.picNameNr)+'.jpg'
        picName =self.log_folder_path + '/' + filStr
        self.picNameNr += 1
        res = cv2.resize(f, (320, 240), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(picName, res)

    def showCamera(self):
        r, f = self.camera.read()
        if r:
            show_image = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
            show_image = QtGui.QImage(show_image.data, show_image.shape[1], show_image.shape[0], QImage.Format_RGB888)
            self.lable_camera.setPixmap(QtGui.QPixmap.fromImage(show_image).scaled(320, 240, QtCore.Qt.KeepAspectRatio))
        return f

    def set_runtime_mode(self):

        self.btnOpen.setDisabled(True)
        self.left_button.setDisabled(True)
        self.right_button.setDisabled(True)
        self.btnStop.setDisabled(True)

        self.btnPlay.setDisabled(False)
        self.btnPlay.setIcon(self.iconPlay)
        self.timeSlider.setDisabled(True)

        self.isOnlineMode = True

    def set_simulink_logfile_mode(self):
        self.btnPlay.setDisabled(True)
        self.timeSlider.setDisabled(False)
        self.btnOpen.setDisabled(False)
        self.isOnlineMode = False

    def RunModeChange(self, index):
        if index == 0:  # log文件读取
            self.set_simulink_logfile_mode()
        else:  # 实时数据采集
            self.set_runtime_mode()

    # 快进
    def up_time(self):
        self.readRadarLogFileThread.logFile.next_line()
        self.readRadarLogFileThread.resume()

    def down_time(self):
        self.readRadarLogFileThread.logFile.goback_oneStep()
        self.readRadarLogFileThread.logFile.set_Progress(self.readRadarLogFileThread.logFile.currLineNr)
        self.readRadarLogFileThread.resume()

    @pyqtSlot()  ##打开文件
    def on_btnOpen_clicked(self):
        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "选择视频文件"
        # filt = "视频文件(*.wmv *.avi *.mp4);;所有文件(*.*)"
        filt = "log file(*.hex);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        if (fileName == ""):
            return
        if self.readRadarLogFileThread:
            self.readRadarLogFileThread.terminate()
            self.readRadarLogFileThread = None


        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.fileName()
        ##      baseName=os.path.basename(fileName)
        self.fileName.setText(baseName)

        curPath = fileInfo.absolutePath()
        QDir.setCurrent(curPath)  # 重设当前目录

        self.readRadarLogFileThread = threadMngt.ReadRadarLogFileThread(fileName)
        self.readRadarLogFileThread.log_pcl_signal.connect(self.show_pcl)  # 仿真文件数据
        self.readRadarLogFileThread.log_obj_signal.connect(self.show_objects)  # 仿真文件数据
        self.readRadarLogFileThread.log_objInfo_signal.connect(self.show_objectsInfo)  # 表格控件
        self.readRadarLogFileThread.log_showPic_signal.connect(self.show_one_pic) # 回放一张图片
        self.readRadarLogFileThread.start()



        self.isRunning = True
        self.btnPlay.setDisabled(False)
        self.btnStop.setDisabled(False)
        self.btnOpen.setDisabled(True)
        self.btnPlay.setIcon(self.iconPause)

        self.init_timeSlider()

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
                self.timer_sensor_show.start(ConfigConstantData.timer_online_sensor_show_and_log_ms)

        else:  # log文件读取
            if self.isRunning:
                self.readRadarLogFileThread.pause()
                self.left_button.setDisabled(False)
                self.right_button.setDisabled(False)
                self.btnOpen.setDisabled(False)
                self.btnPlay.setIcon(self.iconPlay)
            else:
                self.readRadarLogFileThread.resume()
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
