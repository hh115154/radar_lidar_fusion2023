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
        MainWindow.resize(1160, 613)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./images/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)


        self.base_verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.top_horizontalLayout = QtWidgets.QHBoxLayout()
        self.lable1 = QtWidgets.QLabel()
        self.lable2 = QtWidgets.QLabel()
        self.lable3 = QtWidgets.QLabel()
        self.lable4 = QtWidgets.QLabel()

        self.top_horizontalLayout.addWidget(self.lable1)
        self.top_horizontalLayout.addWidget(self.lable2)

        self.bottom_horizontalLayout = QtWidgets.QHBoxLayout()
        self.bottom_horizontalLayout.addWidget(self.lable3)
        self.bottom_horizontalLayout.addWidget(self.lable4)

        self.base_verticalLayout.addLayout(self.top_horizontalLayout)
        self.base_verticalLayout.addLayout(self.bottom_horizontalLayout)

        # 创建一个GroupBox组
        self.groupBox = QGroupBox("图层选项")
        self.groupBox.setFlat(False)

        # 创建复选框1，并默认选中，当状态改变时信号触发事件
        self.checkBox_pic = QCheckBox("图像")
        self.checkBox_pic.setChecked(True)

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
        self.groupBox.setLayout(self.checkBox_layout)
        self.bottom_horizontalLayout.addWidget(self.groupBox)


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
