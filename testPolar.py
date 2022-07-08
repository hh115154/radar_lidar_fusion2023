import sys
from PyQt5.QtWidgets import *

class QStackedWidgetDemo(QMainWindow):
    def __init__(self):
        super(QStackedWidgetDemo, self).__init__()

        self.resize(400, 150)
        #设置窗口标题
        self.setWindowTitle("QStackedWidgetDemo")

        #创建列表窗口，添加条目
        listWidget = QListWidget()
        listWidget.insertItem(0,'联系方式')
        listWidget.insertItem(1,'个人信息')
        listWidget.insertItem(2,'教育程度')
        listWidget.currentRowChanged.connect(self.rowChanged)

        #创建三个小控件
        stack1 = QLabel('标签一',self)
        stack2 = QLabel('标签二',self)
        stack3 = QLabel('标签三',self)

        #在QStackedWidget对象中填充了三个子控件
        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.addWidget(stack1)
        self.stackedWidget.addWidget(stack2)
        self.stackedWidget.addWidget(stack3)

        layout = QHBoxLayout()
        layout.addWidget(listWidget)
        layout.addWidget(self.stackedWidget)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        self.setCentralWidget(mainFrame)

    def rowChanged(self, i):
        self.stackedWidget.setCurrentIndex(i)

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QStackedWidgetDemo()
    main.show()
    sys.exit(app.exec_())

