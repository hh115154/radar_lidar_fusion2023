# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2018年11月5日
@author: Irony
@site: https://pyqt5.com https://github.com/892768447
@email: 892768447@qq.com
@file: JumpSlider
@description: 
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QStyleOptionSlider, QStyle, QWidget, \
    QFormLayout, QLabel

__Author__ = """By: Irony
QQ: 892768447
Email: 892768447@qq.com"""
__Copyright__ = "Copyright (c) 2018 Irony"
__Version__ = "Version 1.0"


class JumpSlider(QSlider):

    def mousePressEvent(self, event):
        # 获取上面的拉动块位置
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        rect = self.style().subControlRect(
            QStyle.CC_Slider, option, QStyle.SC_SliderHandle, self)
        if rect.contains(event.pos()):
            # 如果鼠标点击的位置在滑块上则交给Qt自行处理
            super(JumpSlider, self).mousePressEvent(event)
            return
        if self.orientation() == Qt.Horizontal:
            # 横向，要考虑invertedAppearance是否反向显示的问题
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                event.x() if not self.invertedAppearance() else (self.width(
                ) - event.x()), self.width()))
        else:
            # 纵向
            self.setValue(self.style().sliderValueFromPosition(
                self.minimum(), self.maximum(),
                (self.height() - event.y()) if not self.invertedAppearance(
                ) else event.y(), self.height()))


class TestWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        layout = QFormLayout(self)

        self.label1 = QLabel('0', self)
        layout.addRow(self.label1, JumpSlider(Qt.Horizontal, valueChanged=lambda v: self.label1.setText(str(v))))

        # 横向-反向显示
        self.label2 = QLabel('0', self)
        layout.addRow(self.label2, JumpSlider(Qt.Horizontal, invertedAppearance=True,
                                              valueChanged=lambda v: self.label2.setText(str(v))))

        self.label3 = QLabel('0', self)
        layout.addRow(self.label3,
                      JumpSlider(Qt.Vertical, minimumHeight=200, valueChanged=lambda v: self.label3.setText(str(v))))

        # 纵向反向显示
        self.label4 = QLabel('0', self)
        layout.addRow(self.label4, JumpSlider(Qt.Vertical, invertedAppearance=True, minimumHeight=200,
                                              valueChanged=lambda v: self.label4.setText(str(v))))


if __name__ == '__main__':
    import sys
    import cgitb

    # sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication

#log
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec_())

