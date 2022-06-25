# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
import pyqtgraph.opengl as gl
from OpenGL.GL import *
from PyQt5 import QtGui
import math
import numpy as np

import presentationLayer
import protocol
from PyQt5.QtChart import QChartView, QValueAxis, QPolarChart, QChart


class MyGLAxisItem(gl.GLAxisItem):
    def paint(self):  # 重写线宽
        glLineWidth(4.0)
        super(MyGLAxisItem, self).paint()


# class MyGLGridItem(gl.GLGridItem):
# 	def paint(self):  # 增加同心圆
# 		super(MyGLGridItem, self).paint()
#
# 		x, y, z = self.size()
# 		xs, ys, zs = self.spacing()
# 		# x_vals = np.arange(-x / 2., x / 2. + xs * 0.001, xs)
# 		x_vals = np.arange(-x / 2., x / 2. + xs * 0.001, xs/4)
# 		for r in 2*x_vals:
# 			if r > 0:
# 				# point_step = 0.0
# 				# while point_step < 2 * math.pi:
# 				fov = math.pi/3 + math.pi/10
# 				point_step = - fov/2
# 				while point_step < fov/2 :
# 					xr = r * math.sin(point_step)
# 					yr = r * math.cos(point_step)
# 					glBegin(GL_POINTS)
# 					glVertex2f(xr, yr - 40)
# 					glEnd()
# 					point_step += 0.05
class MyGLGridItem(gl.GLGridItem):
    def __init__(self, size=(5, 5, 1), _step=1, y_offset=0):
        super(MyGLGridItem, self).__init__(size=size)
        x, y, z = self.size()
        self.step =int(_step)
        self.setSpacing(_step, _step, 1)
        self.width = int(x)
        self.length = int(y)
        self.y_offset = y_offset




class MyGLViewWidget(gl.GLViewWidget):
    def __init__(self, parent=None, devicePixelRatio=None, rotationMethod='euler'):
        super(MyGLViewWidget, self).__init__(parent, devicePixelRatio, rotationMethod)
        # car info
        vehicle_length = 4
        vehicle_width = 2
        vehicle_height = 2

        self.grid_length = 50#300
        self.grid_width = 30#200
        self.gridStep = 5

        self.y_offset = -self.grid_length / 2

        # self.grd = MyGLGridItem(size=QtGui.QVector3D(self.grid_width, self.grid_length, 0), _step=self.gridStep,
		# 						y_offset=self.y_offset)
        self.grd = gl.GLGridItem(size=QtGui.QVector3D(self.grid_width, self.grid_length, 0))
        self.grd.setSpacing(self.gridStep, self.gridStep, 1)

        self.addItem(self.grd)


        self.points = []
        self.boxes = []
        self.objIDs = []
        self.lelane = []
        self.rilane = []

        # self.ax = MyGLAxisItem(size=QtGui.QVector3D(0.5, 0.5, 0.5))
        # self.addItem(self.ax)


        camera_distance = 28 #280
        camera_elevation= np.degrees(0.4)


        self.setCameraPosition(distance=camera_distance, elevation=camera_elevation , azimuth=np.degrees(-3.14 / 2))

        self.myCar = gl.GLBoxItem(size=QtGui.QVector3D(vehicle_width, vehicle_length, vehicle_height),
                                  color=QtGui.QColor(255, 255, 0))
        self.myCar.translate(-vehicle_width / 2, self.y_offset - vehicle_length, 0)
        self.addItem(self.myCar)
        self.addDistText()
        self.paintCircles()
        self.paintFOV()

    def paintFOV(self):
        fov = math.pi / 3 + math.pi / 10
        r0 = self.gridStep / 4
        r1 = self.grid_length
        x0 = r0 * math.sin(- fov / 2)
        y0 = r0 * math.cos(- fov / 2) + self.y_offset
        x1 = r1 * math.sin(- fov / 2)
        y1 = r1 * math.cos(- fov / 2) + self.y_offset
        x2 = r0 * math.sin(fov / 2)
        y2 = r0 * math.cos(fov / 2) + self.y_offset
        x3 = r1 * math.sin(fov / 2)
        y3 = r1 * math.cos(fov / 2) + self.y_offset
        posn=[(x0,y0,0),(x1,y1,0)]
        line = gl.GLLinePlotItem(pos=posn, color=QtGui.QColor(255, 255, 255), width=3)
        self.addItem(line)
        posn = [(x2, y2, 0), (x3, y3, 0)]
        line = gl.GLLinePlotItem(pos=posn, color=QtGui.QColor(255, 255, 255), width=3)
        self.addItem(line)

    def paintCircles(self):
        size = 2
        posn = []
        for r in range(0, self.grid_length + self.gridStep, 2 * self.gridStep):
            fov = math.pi / 3 + math.pi / 10
            point_step = - fov / 2
            while point_step < fov / 2:
                xr = r * math.sin(point_step)
                yr = r * math.cos(point_step) - self.grid_length/2
                posn.append((xr, yr,0))
                point_step += 1 / (r + 20)

        points = gl.GLScatterPlotItem(pos=posn, size=size, color=presentationLayer.MyColor.White, pxMode=True)
        self.addItem(points)


    def paint_lane(self, param):
        size = 2
        posn = []
        for i in np.arange(0, 100, 1):
            x = i
            y = param[2] * x * x + param[1] * x + param[0]
            posn.append((y, x + self.f_ElevationAngle, 0))
        color = (1, 1, 1, 1)
        lane = gl.GLScatterPlotItem(pos=posn, size=size, color=color, pxMode=False)
        return lane

    def updatRoadLane(self, le, ri):
        if self.lelane:
            self.removeItem(self.lelane)
        self.lelane = self.paint_lane(le)
        self.addItem(self.lelane)

        if self.rilane:
            self.removeItem(self.rilane)
        self.rilane = self.paint_lane(ri)
        self.addItem(self.rilane)

    def add3Dbox(self, pos, size, color, _id, colorType):
        x,y,z = pos
        box = gl.GLBoxItem(size=size, color=color)
        pos = list(np.sum([pos, (0, self.y_offset, 0)], axis=0))

        z =round(z,2)
        dist =round(y,2)
        strType = presentationLayer.map_color2String[colorType]
        objText = str(_id) + ':' + str(z) + ':' + str(dist) + ':' + strType
        textItem = gl.GLTextItem(text=objText, color=color)
        textItem.setData(font=QtGui.QFont('Helvetica', 8))
        textItem.translate(*pos)
        self.addItem(textItem)
        self.objIDs.append(textItem)

        box.translate(*pos)
        self.addItem(box)
        self.boxes.append(box)

    def clear3Dbox(self):
        if self.boxes:
            for box in self.boxes:
                self.removeItem(box)
            self.boxes = []

        if self.objIDs:
            for objID in self.objIDs:
                self.removeItem(objID)
            self.objIDs = []

    def addPointsDict(self):
        for point in self.points:
            self.addItem(point)

    def addPoints(self, pos, size, color):
        offset_pos = []
        for pos1 in pos:
            x,y,z = pos1
            y+=self.y_offset
            offset_pos.append((x,y,z))

        self.points.append(gl.GLScatterPlotItem(pos=offset_pos, size=size, color=color, pxMode=False))

    def removePoints(self):
        if self.points:
            for point in self.points:
                self.removeItem(point)
            self.points = []

    # if self.points:
    # 	self.removeItem(self.points)
    # 	self.points = []

    def addDistText(self):
        for i in range(0, self.grid_length + self.gridStep, self.gridStep):
            textItem = gl.GLTextItem(text=str(i), color=QtGui.QColor(255, 255, 255))
            textItem.setData(font=QtGui.QFont('Helvetica', 10))
            textItem.translate(-self.grid_width / 2, i -self.grid_length/2, 0)
            self.addItem(textItem)

# if __name__ == "__main__":
# 	import sys
# 	from PyQt5.QtWidgets import *
#
# 	app = QApplication(sys.argv)
#
# 	control = MyGLViewWidget()
# 	control.show()
#
# 	sys.exit(app.exec_())
