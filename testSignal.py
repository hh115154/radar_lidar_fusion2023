import os
os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'
import sys

from PyQt5 import QtCore, QtMultimedia, QtMultimediaWidgets, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    """A window that displays a graphics scene in a central graphics view."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.graphicsScene = QtWidgets.QGraphicsScene()
        self.graphicsScene.setSceneRect(0, 0, 800, 600)
        self.graphicsView = QtWidgets.QGraphicsView()
        self.graphicsView.setScene(self.graphicsScene)
        self.setCentralWidget(self.graphicsView)


class GraphicsVideoItem(QtMultimediaWidgets.QGraphicsVideoItem):
    """An item that displays a video file when added to a graphics scene."""
    def __init__(self, filepath):
        super().__init__()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVideoOutput(self)
        self.player.setMedia(
            QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(filepath)))
        self.player.play()


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()


    filepath = os.path.abspath("log.mp4")
    videoItem = GraphicsVideoItem(filepath)
    mainWindow.graphicsScene.addItem(videoItem)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()