
import sys
from PyQt5.QtCore import QTimer
from datetime import datetime

from PyQt5.QtWidgets import QApplication
import my_util


intv = 1000
timer = QTimer()


def print_time():
    print(my_util.get_timestamp_str())
    t = timer.interval()
    timer.setInterval(t+500)

if __name__== '__main__':
    app = QApplication(sys.argv)
    timer.timeout.connect(print_time)
    timer.start(intv)

    sys.exit(app.exec_())


