import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from socket import *
import struct
import protocol
from PyQt5.QtCore import QThread

port = 42102
pcIp = ''
pcAddr = (pcIp, port)

group_ip = '224.0.2.2'

#定义一个线程类


class New_Thread(QThread):
    def __init__(self, parent=None):
        super(New_Thread, self).__init__(parent)
        self.bRunning = False

    #run函数是子线程中的操作，线程启动后开始执行
    def run(self):
        mySocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        # mySocket = socket(AF_INET, SOCK_STREAM)
        # 绑定 端口号，端口号不能改
        mySocket.bind(pcAddr)

        # 加入组播组
        mreq = struct.pack("=4sl", inet_aton(group_ip), INADDR_ANY)
        mySocket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

        while True:
            if self.bRunning:
                try:
                    recv_message, client = mySocket.recvfrom(65536)
                    if 9401 == len(recv_message):  # objects
                        data = struct.unpack('>9401B', recv_message)
                        bytes_data = int.from_bytes(data, byteorder='big').to_bytes(9401, byteorder='big')
                        obj_buf = bytes_data[16:9385 + 16]
                        obj_list = protocol.ARS548_ObjectList(obj_buf)
                        print('-----------------------obj start--------------------')
                        for obj in obj_list.ObjectList_Objects:
                            print('-----------------------one obj--------------------')
                            print(obj)
                        print('-----------------------obj end--------------------')

                    elif 35336 == len(recv_message):  # pcl
                        data = struct.unpack('>35336B', recv_message)
                        bytes_data = int.from_bytes(data, byteorder='big').to_bytes(35336, byteorder='big')
                        buf = bytes_data[16:35305 + 16]
                        dList = protocol.ARS548_DetectionList(buf)
                        print('-----------------------pcl start--------------------')
                        for pcl in dList.List_Detections:
                            print('------------a point-----------------')
                            print(pcl)
                        print('------------------pcl end-----------------------------------')
                except Exception as e:
                    print(e)



class fileDialogdemo(QWidget):
    def __init__(self,parent=None):
        super(fileDialogdemo, self).__init__(parent)


        #垂直布局
        layout=QVBoxLayout()
        self.recvThd = New_Thread()
        self.recvThd.start()

        #创建按钮，绑定自定义的槽函数，添加到布局中
        self.btn=QPushButton("开始")

        self.btn.clicked.connect(self.changeSt)
        layout.addWidget(self.btn)


        #设置主窗口的布局及标题
        self.setLayout(layout)


    def changeSt(self):
        self.recvThd.bRunning = not self.recvThd.bRunning

        if  self.recvThd.bRunning:
            self.btn.setText("||")
        else:
            self.btn.setText(">>")


if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=fileDialogdemo()
    ex.show()
    sys.exit(app.exec_())