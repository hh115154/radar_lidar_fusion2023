
import sys
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QWidget, QApplication
import cv2
import base64
import io
from PIL import Image

class Demo(QWidget):
    def __init__(self):
        super().__init__()
        pix = QPixmap('sexy.jpg')

        lb1 = QLabel(self)
        lb1.setGeometry(0,0,500,210)
        lb1.setStyleSheet("border: 2px solid red")
        lb1.setPixmap(pix)

        lb2 = QLabel(self)
        lb2.setGeometry(0,250,500,210)
        lb2.setPixmap(pix)
        lb2.setStyleSheet("border: 2px solid red")
        lb2.setScaledContents(True)   #自适应QLabel大小

        self.lb3 = QLabel(self)
        self.lb3.setGeometry(0, 500, 500, 210)
        self.lb3.setPixmap(pix)
        self.lb3.setStyleSheet("border: 2px solid red")
        self.lb3.setScaledContents(True)  # 自适应QLabel大小

def set_img_on_label(lb, img_b64):
    img_b64decode = base64.b64decode(img_b64)  #[21:]
    img_io = io.BytesIO(img_b64decode)
    img=Image.open(img_io)
    pix = img.toqpixmap()
    lb.setScaledContents(True)  # 自适应QLabel大小
    lb.setPixmap(pix)
import logFileMngt
if __name__== '__main__':
    app = QApplication(sys.argv)
    # icon = QIcon("logo.ico")
    # app.setWindowIcon(icon)
    win = Demo()
    win.show()
    frame = []
    for i in range(7539, 8397):
      picName = "./log/Record_2021-10-14_16-43-39_Frame_" + str(i) + ".jpg"
      pix = QPixmap(picName)
      win.lb3.setPixmap(pix)
      cv2.waitKey(1)


    sys.exit(app.exec_())


