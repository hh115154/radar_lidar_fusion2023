# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
import sys
import os.path
import testMainWindow_Ui
import time
import mySocket
import protocol
from PyQt5.QtCore import QThread, pyqtSignal,QTimer,QDateTime
from PyQt5 import QtCore,QtGui
import pyqtgraph.opengl as gl
import pyqtgraph

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


        self.GLView_OrgRadar.setCameraPosition(elevation=90)
        self.GLView_OrgRadar.setCameraParams(fov=90)

        self.GLView_FuseRadar.setCameraPosition(elevation=90)
        self.GLView_FuseRadar.setCameraParams(fov=90)

        self.splitter_vedio_pcl.setFixedSize(100,0)

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

        # 快进
        self.right_button.clicked.connect(self.up_time)
        # 快退
        self.left_button.clicked.connect(self.down_time)

        self.cb.currentIndexChanged.connect(self.RunModeChange)

        # self.camera = None  # QCamera对象
        # cameras = QCameraInfo.availableCameras()  # list[QCameraInfo]
        # if len(cameras) > 0:
        #     self.__iniCamera()  # 初始化摄像头
            # self.__iniImageCapture()  # 初始化静态画图

        self.set_simulink_logfile_mode()

        ###########old code############
        self.radar_timer_step = ConfigConstantData.timer_readlogfile_ms
        self.timer_radar = QtCore.QTimer()  # 控制雷达的刷新频率
        self.timer_radar.timeout.connect(self.resume_logThread)
        self.timer_radar.start(self.radar_timer_step)

        # self.cameraThread = threadMngt.VideoRecordThread()
        # self.cameraThread.start()
        # self.cameraThread.pause()
        self.orgRadarThread = threadMngt.OriginalRadarThread()
        self.orgRadarThread.orgRadar_pcl_signal.connect(self.show_radar)  # 仿真文件数据
        self.orgRadarThread.orgRadar_obj_signal.connect(self.show_objects)  # 仿真文件数据
        self.orgRadarThread.orgRadar_objInfo_signal.connect(self.show_objectsInfo) # 表格控件
        self.orgRadarThread.start()

        self.timer_online_updatecamera = QtCore.QTimer()
        self.timer_online_updatecamera.timeout.connect(self.update_online_camera)

        self.timeSlider.valueChanged.connect(self.on_timeslider_valueChanged)
        self.timeSlider.sliderReleased.connect(self.on_timeslider_valueChanged)

        self.total_time_s = 0

        self.set_default_mode()

        self.readRadarLogFileThread = 0

        ########new code##############
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
        if self.timeSlider.isSliderDown() and not self.isRunning:
            return  # 如果正在拖动滑条，退出
        if abs(self.timeSlider.value() - self.timeSlider_oldValue) > 10:
            newLogFileLineNr =int(self.readRadarLogFileThread.logFile.log_file_size * self.timeSlider.value()/self.timeSlider.maximum())
            self.readRadarLogFileThread.logFile.set_Progress(newLogFileLineNr)
            if not self.isRunning:
                self.readRadarLogFileThread.resume()

        self.timeSlider_oldValue = self.timeSlider.value()

    def set_default_mode(self):
        self.isRunning = False
        self.isOnlineMode = True
        self.cb.setCurrentIndex(1)
        self.btnPlay.setDisabled(False)
        self.btnStop.setDisabled(True)
        self.left_button.setDisabled(True)
        self.right_button.setDisabled(True)
        self.timeSlider.setDisabled(True)
        self.cb.setDisabled(False)

    def update_online_camera(self):
        pass
        # show_image = self.cameraThread.showImage
        # self.lable_camera.setPixmap(QtGui.QPixmap.fromImage(show_image))

    def show_radar(self, dict):
        self.GLView_OrgRadar.removePoints()
        for key in dict.keys():
            self.GLView_OrgRadar.addPoints(pos=dict[key], size=1, color=map_hight_color[key])
        self.GLView_OrgRadar.addPointsDict()

        self.update_log_progress()

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

    def resume_logThread(self):
        if not self.isOnlineMode and self.isRunning:
            picName = self.readRadarLogFileThread.logFile.getNextPic()
            self.show_one_pic(picName)
            self.readRadarLogFileThread.resume()

    def get_specific_line(self):
        if not self.isOnlineMode and self.isRunning:
            self.readRadarLogFileThread.pause()

    # def __iniCamera(self):
    #     camInfo = QCameraInfo.defaultCamera()  # 获取缺省摄像头,QCameraInfo
    #
    #     self.camera = QCamera(camInfo)  # 创建摄像头对象
    #     self.camera.setViewfinder(self.viewFinder)  # 设置取景框预览
    #
    #     self.camera.setCaptureMode(QCamera.CaptureVideo)


    def set_runtime_mode(self):
        self.videoWidget.setHidden(True)
        self.videoWidget.setDisabled(True)
        # self.viewFinder.setHidden(False)
        # self.viewFinder.setDisabled(False)
        self.lable_camera.setHidden(False)
        self.lable_camera.setDisabled(False)

        self.btnOpen.setDisabled(True)
        self.left_button.setDisabled(True)
        self.right_button.setDisabled(True)
        self.btnStop.setDisabled(True)

        self.btnPlay.setDisabled(False)
        self.btnPlay.setIcon(self.iconPlay)
        self.timeSlider.setDisabled(True)

        self.isOnlineMode = True


    def set_simulink_logfile_mode(self):
        # self.viewFinder.setHidden(True)
        # self.viewFinder.setDisabled(True)
        # self.lable_camera.setHidden(True)
        # self.lable_camera.setDisabled(True)
        self.videoWidget.setHidden(False)
        self.videoWidget.setDisabled(False)
        self.btnPlay.setDisabled(True)
        # self.left_button.setDisabled(False)
        # self.right_button.setDisabled(False)
        self.timeSlider.setDisabled(False)
        self.btnOpen.setDisabled(False)
        # self.btnPlay.setDisabled(False)
        # self.btnStop

        # self.camera.stop()
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
        lineNr =  self.readRadarLogFileThread.logFile.goback_oneStep()
        self.readRadarLogFileThread.logFile.set_Progress(lineNr)
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
        self.readRadarLogFileThread.log_pcl_signal.connect(self.show_radar)  # 仿真文件数据
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
        # print(picFullPath)

        # self.lable_camera.resize(320, 240)

        # 加载图片,并自定义图片展示尺寸
        image = QtGui.QPixmap(picFullPath).scaled(320, 320)
        # 显示图片
        self.lable_camera.setPixmap(image)


        # # 通过cv读取图片
        # img = cv2.imread(picFullPath)
        # # 通道转化
        # RGBImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # # 将图片转化成Qt可读格式
        # image = QtGui.QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], QtGui.QImage.FormatRGB888)
        #
        # # 加载图片,并自定义图片展示尺寸
        # image = QtGui.QPixmap(image).scaled(640, 480)
        # # 显示图片
        # self.lable_camera.setPixmap(image)

    @pyqtSlot()  ##播放
    def on_btnPlay_clicked(self):
        if self.isOnlineMode:  # 实时数据采集
            if self.isRunning:  # 如果正在运行，则暂停，并保存文件
                # self.camera.stop()
                self.timer_online_updatecamera.stop()
                # self.cameraThread.pause()
                # self.cameraThread.saveVideo()

                self.orgRadarThread.pause()
                # self.cameraThread.quit()
                self.btnPlay.setIcon(self.iconPlay)
            else:  # 如果没有运行，则开始记录
                # self.camera.start()
                # if self.cameraThread.videoWriter is None:
                #     self.cameraThread.updateVideoWriter()
                # self.cameraThread.resume()
                self.timer_online_updatecamera.start(50)
                self.orgRadarThread.resume()
                self.btnPlay.setIcon(self.iconPause)
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
        # md.GLView_FuseRadar.removeItem(md.GLView_FuseRadar.points)  # 当w使用addItem()后，才会生效显示图像
        md.GLView_FuseRadar.removePoints()

    def slot_print(self, value):
        print(value)
        # pos = self.GLView_FuseRadar.cameraPosition()
        # print(pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    md = MyController()
    md.showMaximized()
    md.show()

    sys.exit(app.exec_())
