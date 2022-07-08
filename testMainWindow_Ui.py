# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03


# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import myControls
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QCameraViewfinder

import ConfigConstantData

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1160, 613)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # 主垂直布局
        self.base_verticalLayout = QtWidgets.QVBoxLayout()

        # 嵌套一层垂直布局
        play_area_verticalLayout = QtWidgets.QVBoxLayout()

        # 最下面的水平布局，存放几个按钮
        btns_area_horizontallayout = QtWidgets.QHBoxLayout()

        if ConfigConstantData.MachineType == ConfigConstantData.radar4D_548:
            # 主分隔条，左右分隔
            self.splitter_org_obj = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
            # 竖向第二条分割拖动条
            self.splitter_glview_table = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

            #left
            self.splitter_vedio_pcl = QtWidgets.QSplitter(QtCore.Qt.Vertical)

            #left.top - 左上角视频
            self.lable_camera = QtWidgets.QLabel() # 显示离线图片
            self.lable_camera.setObjectName("lable_camera")
            self.lable_camera.setScaledContents(True)

            self.splitter_vedio_pcl.addWidget(self.lable_camera)

            # 左下角小控件
            self.GLView_OrgRadar = myControls.MyGLViewWidget()
            self.GLView_OrgRadar.setCameraPosition(elevation=90)
            self.GLView_OrgRadar.setCameraParams(fov=90)
            self.splitter_vedio_pcl.addWidget(self.GLView_OrgRadar)

            self.splitter_org_obj.addWidget(self.splitter_vedio_pcl)

            # 3D空间，显示目标物
            self.GLView_FuseRadar = myControls.MyGLViewWidget()
            self.GLView_FuseRadar.setCameraPosition(elevation=90)
            self.GLView_FuseRadar.setCameraParams(fov=90)

            # 纵向第二个分隔条左边放大3D空间控件
            self.splitter_glview_table.addWidget(self.GLView_FuseRadar)


            self.tableView = QtWidgets.QTableView()
            # 水平方向标签拓展剩下的窗口部分，填满表格
            self.tableView.horizontalHeader().setStretchLastSection(True)
            # 水平方向，表格大小拓展到适当的尺寸
            self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
            self.tableView.verticalHeader().setDefaultSectionSize(38)
            self.splitter_glview_table.addWidget(self.tableView)

            # 主分隔条右侧先放一个分给条
            self.splitter_org_obj.addWidget(self.splitter_glview_table)

            self.base_verticalLayout.addWidget(self.splitter_org_obj)

        elif ConfigConstantData.MachineType == ConfigConstantData.J3System:

            #用于显示多层图片的lable
            self.lable_main = QtWidgets.QLabel()
            self.lable_main.setScaledContents(True)
            self.lable_main.setFixedSize(QtCore.QSize(1900,900))

            play_area_verticalLayout.addWidget(self.lable_main)

            # # 创建一个GroupBox组
            # self.groupBox = QGroupBox("图层选项")
            # self.groupBox.setFlat(False)

            # 创建复选框1，并默认选中，当状态改变时信号触发事件
            self.checkBox_pic = QCheckBox("图像")
            self.checkBox_pic.setChecked(False)

            # 创建复选框，标记状态改变时信号触发事件
            self.checkBox_OrgObj = QCheckBox("目标")
            self.checkBox_OrgObj.setChecked(True)

            # 创建复选框3，设置为3状态，设置默认选中状态为半选状态，当状态改变时信号触发事件
            self.checkBox_Fusion = QCheckBox("融合")
            self.checkBox_Fusion.setChecked(True)

            self.checkBox_layout = QtWidgets.QHBoxLayout()
            self.checkBox_layout.addWidget(self.checkBox_pic)
            self.checkBox_layout.addWidget(self.checkBox_OrgObj)
            self.checkBox_layout.addWidget(self.checkBox_Fusion)
            # self.groupBox.setLayout(self.checkBox_layout)

            btns_area_horizontallayout.addLayout(self.checkBox_layout)


        self.timeSlider = myControls.JumpSlider()
        self.timeSlider.setTracking(True)
        self.timeSlider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")

        play_area_verticalLayout.addWidget(self.timeSlider)
        play_area_verticalLayout.addLayout(btns_area_horizontallayout)


        self.fileName = QtWidgets.QLabel("无文件")
        self.fileName.setMinimumSize(QtCore.QSize(120, 0))
        self.fileName.setObjectName("LabRatio")
        btns_area_horizontallayout.addWidget(self.fileName)

        self.cb = QtWidgets.QComboBox()
        self.cb.addItem("离线文件读取")
        self.cb.addItem("实时数据采集")
        self.cb.setCurrentIndex(1)
        btns_area_horizontallayout.addWidget(self.cb)

        self.btnOpen = QtWidgets.QPushButton()
        self.btnOpen.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/001.GIF"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpen.setIcon(icon)
        self.btnOpen.setObjectName("btnOpen")
        btns_area_horizontallayout.addWidget(self.btnOpen)

        self.left_button = QtWidgets.QPushButton()
        self.left_button.setObjectName("left_button")
        self.iconLeft_button = QtGui.QIcon()
        self.iconLeft_button.addPixmap(QtGui.QPixmap("./images/610.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.left_button.setIcon(self.iconLeft_button)
        btns_area_horizontallayout.addWidget(self.left_button)

        self.btnPlay = QtWidgets.QPushButton()
        self.btnPlay.setEnabled(True)
        self.btnPlay.setText("")
        self.iconPlay = QtGui.QIcon()
        self.iconPlay.addPixmap(QtGui.QPixmap("./images/620.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPlay.setIcon(self.iconPlay)
        self.btnPlay.setObjectName("btnPlay")
        btns_area_horizontallayout.addWidget(self.btnPlay)

        self.right_button = QtWidgets.QPushButton()
        self.right_button.setObjectName("right_button")
        self.icon_right_button = QtGui.QIcon()
        self.icon_right_button.addPixmap(QtGui.QPixmap("./images/612.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.right_button.setIcon(self.icon_right_button)
        btns_area_horizontallayout.addWidget(self.right_button)

        self.iconPause = QtGui.QIcon()
        self.iconPause.addPixmap(QtGui.QPixmap("./images/622.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)


        # self.btnStop = QtWidgets.QPushButton()
        # self.btnStop.setEnabled(False)
        # self.btnStop.setText("")
        # icon3 = QtGui.QIcon()
        # icon3.addPixmap(QtGui.QPixmap("./images/624.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btnStop.setIcon(icon3)
        # self.btnStop.setObjectName("btnStop")
        # btns_area_horizontallayout.addWidget(self.btnStop)

        self.LabRatio = QtWidgets.QLabel("进度")
        self.LabRatio.setMinimumSize(QtCore.QSize(60, 0))
        self.LabRatio.setObjectName("LabRatio")

        self.LabTotal = QtWidgets.QLabel("/")
        self.LabTotal.setMinimumSize(QtCore.QSize(60, 0))
        self.LabTotal.setObjectName("LabRatio")
        btns_area_horizontallayout.addWidget(self.LabRatio)
        btns_area_horizontallayout.addWidget(self.LabTotal)


        self.base_verticalLayout.addLayout(play_area_verticalLayout)
        self.base_verticalLayout.setStretch(0,1)


        self.centralwidget.setLayout(self.base_verticalLayout)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1160, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("BHAP", "BHAP"))


from PyQt5.QtMultimediaWidgets import QVideoWidget
