# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.Qt import QtCore, QtGui
import myControls
from PyQt5.QtMultimediaWidgets import QCameraViewfinder


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1160, 613)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        #left
        self.splitter_vedio_pcl = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        # verticalLayout = QtWidgets.QVBoxLayout()

        #left.top
        # self.swt_camera_stacklayout = QtWidgets.QStackedLayout()
        self.swt_camera_stackWidget= QtWidgets.QStackedWidget()

        self.videoWidget = QVideoWidget()
        self.videoWidget.setObjectName("videoWidget")

        #
        # self.viewFinder = QCameraViewfinder()
        # self.viewFinder.setMinimumSize(QtCore.QSize(150, 0))
        # self.viewFinder.setObjectName("viewFinder")
        # self.swt_camera_stacklayout.addWidget(self.viewFinder)

        self.lable_camera = QtWidgets.QLabel() # 显示离线图片
        self.lable_camera.setObjectName("lable_camera")
        self.lable_camera.setScaledContents(True)

        self.swt_camera_stackWidget.addWidget(self.lable_camera)
        self.swt_camera_stackWidget.addWidget(self.videoWidget)

        # self.lable_camera.setDisabled(True)
        # self.videoWidget.setDisabled(True)
        self.splitter_vedio_pcl.addWidget(self.swt_camera_stackWidget)

        # splitter_vedio_pcl.addWidget(self.swt_camera_stacklayout)

        # 左下角小控件
        self.GLView_OrgRadar = myControls.MyGLViewWidget()
        self.splitter_vedio_pcl.addWidget(self.GLView_OrgRadar)
        # verticalLayout.setStretch(0,1)
        # verticalLayout.setStretch(1,1)


        # 右侧大控件
        self.splitter_glview_table = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        # self.GLView_FuseRadar = myControls.MyGLViewWidget(rotationMethod="quaternion")
        self.GLView_FuseRadar = myControls.MyGLViewWidget()

        self.splitter_glview_table.addWidget(self.GLView_FuseRadar)

        self.tableView = QtWidgets.QTableView()
        # 水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        # 水平方向，表格大小拓展到适当的尺寸
        # self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode( QtWidgets.QHeaderView.Interactive)

        # # 用户可调整，默认值为setDefaultSectionSized的值
        # table_obj.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # # 用户不可调整，默认值为setDefaultSectionSized的值
        # table_obj.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # # 用户不可调整,自动平分适应可用区域
        # table_obj.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # # 用户不可调整,自动适应内容的宽度
        # table_obj.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # # 用户可调整,默认值为setDefaultSectionSized的值
        # table_obj.horizontalHeader().setSectionResizeMode(QHeaderView.Custom)


        self.tableView.verticalHeader().setDefaultSectionSize(38)
        self.splitter_glview_table.addWidget(self.tableView)

        self.splitter_org_obj = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # horizontalLayout = QtWidgets.QHBoxLayout()
        self.splitter_org_obj.addWidget(self.splitter_vedio_pcl)

        self.splitter_org_obj.addWidget(self.splitter_glview_table)
        # horizontalLayout.setStretch(0,1)
        # horizontalLayout.setStretch(1,2)

        self.base_verticalLayout = QtWidgets.QVBoxLayout()
        self.base_verticalLayout.addWidget(self.splitter_org_obj)

        play_area_verticalLayout = QtWidgets.QVBoxLayout()
        self.timeSlider = QtWidgets.QSlider()
        self.timeSlider.setTracking(True)
        # self.timeSlider.setMaximum(99)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")

        play_area_verticalLayout.addWidget(self.timeSlider)

        btns_area_horizontallayout = QtWidgets.QHBoxLayout()
        btns_area_horizontallayout.setObjectName("btnshorizontalLayout")


        self.fileName = QtWidgets.QLabel("无文件")
        self.fileName.setMinimumSize(QtCore.QSize(120, 0))
        self.fileName.setObjectName("LabRatio")
        btns_area_horizontallayout.addWidget(self.fileName)

        self.cb = QtWidgets.QComboBox()
        self.cb.addItem("离线文件读取")
        self.cb.addItem("实时数据采集")
        btns_area_horizontallayout.addWidget(self.cb)

        self.btnOpen = QtWidgets.QPushButton()
        self.btnOpen.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/001.GIF"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpen.setIcon(icon)
        self.btnOpen.setObjectName("btnOpen")
        btns_area_horizontallayout.addWidget(self.btnOpen)

        self.left_button = QtWidgets.QPushButton("<<")
        self.left_button.setObjectName("left_button")
        btns_area_horizontallayout.addWidget(self.left_button)

        self.btnPlay = QtWidgets.QPushButton()
        self.btnPlay.setEnabled(True)
        self.btnPlay.setText("")
        self.iconPlay = QtGui.QIcon()
        self.iconPlay.addPixmap(QtGui.QPixmap("./images/620.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPlay.setIcon(self.iconPlay)
        self.btnPlay.setObjectName("btnPlay")
        btns_area_horizontallayout.addWidget(self.btnPlay)

        self.right_button = QtWidgets.QPushButton(">>")
        self.right_button.setObjectName("right_button")
        btns_area_horizontallayout.addWidget(self.right_button)

        self.iconPause = QtGui.QIcon()
        self.iconPause.addPixmap(QtGui.QPixmap("./images/622.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)


        self.btnStop = QtWidgets.QPushButton()
        self.btnStop.setEnabled(False)
        self.btnStop.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./images/624.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStop.setIcon(icon3)
        self.btnStop.setObjectName("btnStop")
        btns_area_horizontallayout.addWidget(self.btnStop)

        self.LabRatio = QtWidgets.QLabel("进度")
        self.LabRatio.setMinimumSize(QtCore.QSize(120, 0))
        self.LabRatio.setObjectName("LabRatio")
        btns_area_horizontallayout.addWidget(self.LabRatio)

        play_area_verticalLayout.addLayout(btns_area_horizontallayout)
        self.base_verticalLayout.addLayout(play_area_verticalLayout)
        self.base_verticalLayout.setStretch(0,1)


        self.centralwidget.setLayout(self.base_verticalLayout)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1160, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("BHAP", "BHAP"))


from PyQt5.QtMultimediaWidgets import QVideoWidget
