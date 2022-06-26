#!

import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi


class fileClass(QMainWindow):
    def __init__(self):
        super(fileClass, self).__init__()
        self.initUI()
        self.fname = []

    def initUI(self):
        self.uipage = loadUi('./fileUI.ui', self)
        self.uipage.actionOpen.triggered.connect(self.openFileHandle)
        self.uipage.actionSave.triggered.connect(self.saveFileHandle1)

    def openFileHandle(self):
        print('open file')
        self.fname = QFileDialog.getOpenFileName(self, 'Open File', './', 'Txt (*.txt)')
        if self.fname[0]:
            with open(self.fname[0], 'r', encoding='utf-8') as f:
                self.uipage.plainTextEdit.setPlainText(f.read())
                f.close()

    def saveFileHandle(self):
        print('save file')
        self.fname = QFileDialog.getSaveFileName(self, 'Write File', './', 'All(*.*)')
        if self.fname[0]:
            with open(self.fname[0], 'w', encoding='utf-8') as f:
                datatmp = self.uipage.plainTextEdit.toPlainText()
                f.write(datatmp)
                f.close()

    def saveFileHandle1(self):
        try:
            if self.fname[0]:
                with open(self.fname[0], 'w', encoding='utf-8') as f:
                    datatmp = self.uipage.plainTextEdit.toPlainText()
                    f.write(datatmp)
                    f.close()
        except:
            print('请先打开文件')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = fileClass()
    mw.show()
    sys.exit(app.exec_())