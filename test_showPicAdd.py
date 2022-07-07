# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/7/7 10:21
# @File     : test_showPicAdd.py
# @Project  : radar_fusion
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QApplication
import numpy as np
import test_picadd
import cv2


class MyController(QMainWindow, test_picadd.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyController, self).__init__()
        self.setupUi(self)
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # QCamera对象

        self.pic_shape = (480, 640, 3)
        self.black_board = np.zeros(self.pic_shape, dtype=np.uint8)  # 黑色画布
        self.pic_org =  np.zeros(self.pic_shape, dtype=np.uint8)  # 黑色画布
        self.pic_meta =  np.zeros(self.pic_shape, dtype=np.uint8)  # 黑色画布
        self.pic_fusion =  np.zeros(self.pic_shape, dtype=np.uint8)  # 黑色画布

        self.timer_camera = QtCore.QTimer()  # 控制雷达的刷新频率
        self.timer_camera.timeout.connect(self.show_camera)
        timer_ms = 100
        self.timer_camera.start(timer_ms)


    def update_pic(self,pic):
        x = 100
        y = 200
        w = 30
        h = 40
        class_name = 'test aaa'
        cv2.rectangle(pic, (x, y), (x + w, y + h), (128, 42, 42), 1)  # 画面，左上角坐标，右下角坐标，RGB颜色，厚度
        cv2.putText(pic, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (128, 42, 42), 1)  # 画面，文本内容，位置


    def show_camera(self):
        if self.checkBox_Fusion.isChecked():
            self.update_pic(self.pic_fusion)
        else:
            self.pic_fusion = np.zeros(self.pic_shape, dtype=np.uint8)  # 黑色画布

        #1
        r, f = self.camera.read()
        if r:
            self.pic_org = f
            self.show_pic_with_lable(self.pic_org,self.lable1)

        #2
        self.show_pic_with_lable(self.pic_fusion,self.lable2)

        #3
        add_pic = cv2.addWeighted(self.pic_org, 1, self.pic_meta, 1, 0)
        self.show_pic_with_lable(add_pic,self.lable3)

        #4
        self.show_pic_with_lable(self.pic_meta,self.lable4)


    def show_pic_with_lable(self,pic,lable):

        temp = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        temp = QtGui.QImage(temp.data, temp.shape[1], temp.shape[0],
                                    QImage.Format_RGB888)
        lable.setPixmap(QtGui.QPixmap.fromImage(temp))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    md = MyController()
    md.showMaximized()
    md.show()

    sys.exit(app.exec_())