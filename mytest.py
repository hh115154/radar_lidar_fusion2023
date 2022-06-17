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

import threadMngt
from PyQt5.QtMultimedia import (QCameraInfo,QCameraImageCapture,
      QImageEncoderSettings,QMultimedia,QVideoFrame,QSound,QCamera)

from PyQt5.QtCore import  pyqtSlot,QUrl,QDir, QFileInfo,Qt,QEvent
from PyQt5.QtMultimedia import QMediaContent,QMediaPlayer

map_hight_color = {1:(0.,0,1,1),
                   2:(0,1,1,1),
                   3:(0,1,0,1),
                   4:(1,1,0,1),
                   5:(1,0,0,1)}
class MyController(QMainWindow, testMainWindow_Ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyController, self).__init__()
        self.setupUi(self)

        self.player = QMediaPlayer(self)  # 创建视频播放器
        self.player_ms_step = 1880
        self.timeSlider.setMaximum(self.player_ms_step*2)
        self.radar_timer_step = 60
        self.radar_lineNr_step = 5
        self.player.setPlaybackRate(0.5)
        self.player.setNotifyInterval(1)  # 信息更新周期, ms

        self.player.setVideoOutput(self.videoWidget)  # 视频显示组件

        self.videoWidget.installEventFilter(self)  # 事件过滤器

        self.__duration = ""
        self.__curPos = ""

        self.player.stateChanged.connect(self.do_stateChanged)
        self.player.positionChanged.connect(self.do_positionChanged)
        self.player.durationChanged.connect(self.do_durationChanged)

        # 快进
        self.right_button.clicked.connect(self.up_time)
        # 快退
        self.left_button.clicked.connect(self.down_time)


        self.cb.currentIndexChanged.connect(self.RunModeChange)

        self.camera = None  # QCamera对象
        cameras = QCameraInfo.availableCameras()  # list[QCameraInfo]
        if len(cameras) > 0:
            self.__iniCamera()  # 初始化摄像头
            # self.__iniImageCapture()  # 初始化静态画图

        self.set_simulink_logfile_mode()
        self.isRunning = False
        self.isOnlineMode = False


        ###########old code############
        self.timer_radar = QtCore.QTimer()  # 控制雷达的刷新频率
        self.timer_radar.timeout.connect(self.get_next_line)
        self.timer_radar.start(self.radar_timer_step)


        ########new code##############



    def read_logFile_from_LineNr(self, lineNr):
        self.readRadarLogFileThread.currLineNr = lineNr
        self.readRadarLogFileThread.resume()

    def show_radar(self, dict):
        self.GLView_OrgRadar.removePoints()
        for key in dict.keys():
            self.GLView_OrgRadar.addPoints(pos=dict[key], size=1, color=map_hight_color[key])
        self.GLView_OrgRadar.addPointsDict()

    def show_objects(self, objPre):
        self.GLView_FuseRadar.clear3Dbox()
        for i in range(len(objPre)):
            size = QtGui.QVector3D(objPre[i].length, objPre[i].width, objPre[i].height)
            self.GLView_FuseRadar.add3Dbox(pos=objPre[i].posn, size=size, color=objPre[i].color, _id=objPre[i].id)

    def get_next_line(self):
        if not self.isOnlineMode and self.isRunning and self.readRadarLogFileThread._isPause:
            self.readRadarLogFileThread.currLineNr += 1
            self.readRadarLogFileThread.resume()

    def get_specific_line(self):
        if not self.isOnlineMode and self.isRunning:
            self.readRadarLogFileThread.pause()

    def __iniCamera(self):
        camInfo = QCameraInfo.defaultCamera()  # 获取缺省摄像头,QCameraInfo
        # self.ui.comboCamera.addItem(camInfo.description())  # 摄像头描述
        # self.ui.comboCamera.setCurrentIndex(0)

        self.camera = QCamera(camInfo)  # 创建摄像头对象
        self.camera.setViewfinder(self.viewFinder)  # 设置取景框预览

        self.camera.setCaptureMode(QCamera.CaptureVideo)

        mode = QCamera.CaptureStillImage
        supported = self.camera.isCaptureModeSupported(mode)
        # self.ui.checkStillImage.setChecked(supported)  # 支持拍照

        supported = self.camera.isCaptureModeSupported(QCamera.CaptureVideo)
        # self.ui.checkVideo.setChecked(supported)  # 支持视频录制

        supported = self.camera.exposure().isAvailable()
        # self.ui.checkExposure.setChecked(supported)  # 支持曝光补偿

        supported = self.camera.focus().isAvailable()
        # self.ui.checkFocus.setChecked(supported)  # 支持变焦

        # self.camera.stateChanged.connect(self.do_cameraStateChanged)

    def set_runtime_mode(self):
        self.videoWidget.setHidden(True)
        self.videoWidget.setDisabled(True)
        self.viewFinder.setHidden(False)
        self.viewFinder.setDisabled(False)

        self.btnOpen.setDisabled(True)
        self.left_button.setDisabled(True)
        self.right_button.setDisabled(True)
        self.camera.start()
        self.isOnlineMode = True


    def set_simulink_logfile_mode(self):
        self.viewFinder.setHidden(True)
        self.viewFinder.setDisabled(True)
        self.videoWidget.setHidden(False)
        self.videoWidget.setDisabled(False)

        self.left_button.setDisabled(False)
        self.right_button.setDisabled(False)
        self.btnOpen.setDisabled(False)
        self.camera.stop()
        self.isOnlineMode = False


    def RunModeChange(self, index):
        if index == 0:  # log文件读取
            self.set_simulink_logfile_mode()
        else:  # 实时数据采集
            self.set_runtime_mode()


    # 快进
    def up_time(self):
        num = self.player.position() + 24#int(self.player.duration() / self.player_ms_step)
        self.player.setPosition(num)
        self.readRadarLogFileThread.resume()

        # if self.player.state() == QMediaPlayer.PausedState:
        #     self.player.setPosition(int(position))
        #     self.player.play()
        #     self.player.pause()


    def down_time(self):
        num = self.player.position() - 24#int(self.player.duration() / self.player_ms_step)
        self.player.setPosition(num)
        self.readRadarLogFileThread.currLineNr -= 4
        self.readRadarLogFileThread.resume()

    def eventFilter(self, watched, event):  ##事件过滤器
        if (watched != self.videoWidget):
            return super().eventFilter(watched, event)

        # 鼠标左键按下时，暂停或继续播放
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                if self.player.state() == QMediaPlayer.PlayingState:
                    self.player.pause()
                else:
                    self.player.play()

        # 全屏状态时，按ESC键退出全屏
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Escape:
                if self.videoWidget.isFullScreen():
                    self.videoWidget.setFullScreen(False)

        return super().eventFilter(watched, event)

    # def update_radar_progress(self, progress):
    #     position =self.player.duration()*progress/self.player_ms_step/2
    #     if self.player.state() == QMediaPlayer.PausedState:
    #     # now= self.player.position()
    #         self.player.setPosition(position)
    #         self.player.resume()
    #         self.player.pause()


        ##  ==========由connectSlotsByName()自动连接的槽函数============

    @pyqtSlot()  ##打开文件
    def on_btnOpen_clicked(self):
        ##      curPath=os.getcwd()  #获取系统当前目录
        curPath = QDir.currentPath()  # 获取系统当前目录
        title = "选择视频文件"
        filt = "视频文件(*.wmv *.avi *.mp4);;所有文件(*.*)"
        fileName, flt = QFileDialog.getOpenFileName(self, title, curPath, filt)
        if (fileName == ""):
            return


        fileInfo = QFileInfo(fileName)
        baseName = fileInfo.fileName()
        ##      baseName=os.path.basename(fileName)
        self.fileName.setText(baseName)


        curPath = fileInfo.absolutePath()
        QDir.setCurrent(curPath)  # 重设当前目录

        media = QMediaContent(QUrl.fromLocalFile(fileName))
        self.player.setMedia(media)  # 设置播放文件
        self.player.play()
        self.isRunning = True
        self.player.pause()
        # self.readRadarLogFileThread.resume()


        self.readRadarLogFileThread = threadMngt.ReadRadarLogFileThread(baseName)
        self.readRadarLogFileThread.log_pcl_signal.connect(self.show_radar)  # 仿真文件数据
        self.readRadarLogFileThread.log_obj_signal.connect(self.show_objects)  # 仿真文件数据
        # self.readRadarLogFileThread.update_progress_signal.connect(self.update_radar_progress)  # 仿真文件数据
        self.readRadarLogFileThread.start()

    @pyqtSlot()  ##播放
    def on_btnPlay_clicked(self):
        if self.isOnlineMode:  # 实时数据采集
            if self.isRunning:  # 如果正在运行，则暂停，并保存文件
                self.player.pause()
            else:  # 如果没有运行，则开始记录
                self.player.play()
        else:  # log文件读取
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()
                self.readRadarLogFileThread.pause()
                self.isRunning = False
            else:
                self.player.play()
                self.readRadarLogFileThread.resume()
                self.isRunning = True

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

    @pyqtSlot()  ##停止
    def on_btnStop_clicked(self):
        self.player.stop()

    @pyqtSlot(int)  ##播放进度调节
    def on_sliderPosition_valueChanged(self, value):
        self.player.setPosition(value)
        print("state is : ",self.player.PlayingState)


    ##  =============自定义槽函数===============================

    def do_stateChanged(self, state):  ##状态变化
        isPlaying = (state == QMediaPlayer.PlayingState)

        if isPlaying:
            self.btnPlay.setIcon(self.iconPause)
        else:
            self.btnPlay.setIcon(self.iconPlay)

        self.btnStop.setEnabled(isPlaying)

    def do_durationChanged(self, duration):  ##文件长度变化
        self.timeSlider.setMaximum(duration)

        secs = duration / 1000  # 秒
        mins = secs / 60  # 分钟
        secs = secs % 60  # 余数秒
        self.__duration = "%02d:%02d" % (mins, secs)
        self.LabRatio.setText(self.__curPos + "/" + self.__duration)


    def do_positionChanged(self, position):  ##当前播放位置变化
        if (self.timeSlider.isSliderDown()):
            return  # 如果正在拖动滑条，退出

        self.timeSlider.setSliderPosition(position)
        secs = position / 1000  # 秒
        mins = secs / 60  # 分钟
        secs = secs % 60  # 余数秒
        self.__curPos = "%02d:%02d" % (mins, secs)
        self.LabRatio.setText(self.__curPos + "/" + self.__duration)

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
