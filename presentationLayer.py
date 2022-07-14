# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
import time
from enum import Enum
from PyQt5 import QtGui
from ctypes import *
import ctypes
import cv2
import numpy as np
class Pcl_Color():
    def __init__(self):
        self.dict_hight2color = {1: [], 2: [], 3: [], 4: [], 5: []}

    def add_point_to_dict(self, posn):
        x, y, z = posn
        if z < -2:
            self.dict_hight2color[1].append(posn)
        elif z < 0:
            self.dict_hight2color[2].append(posn)
        elif z < 2:
            self.dict_hight2color[3].append(posn)
        elif z < 4:
            self.dict_hight2color[4].append(posn)
        else:
            self.dict_hight2color[5].append(posn)

    def clear_dict(self):
        for key in self.dict_hight2color:
            self.dict_hight2color[key] = []


class ObjectType(Enum):
    Car = 0
    Truck = 1
    Motorcycle = 2
    Bicycle = 3
    Pedestrian = 4
    Animal = 5
    Hazard = 6
    Unknown = 7
    Overdrivable = 8
    Underdrivable = 9

map_color2String = {
    ObjectType.Car : 'Car',
    ObjectType.Truck : 'Truck',
    ObjectType.Motorcycle: 'Motorcycle',
    ObjectType.Bicycle : 'Bicycle',
    ObjectType.Pedestrian : 'Pedestrian',
    ObjectType.Animal : 'Animal',
    ObjectType.Hazard : 'Hazard',
    ObjectType.Unknown : 'Unknown',
    ObjectType.Overdrivable : 'Overdrivable',
    ObjectType.Underdrivable : 'Underdrivable'}


class MyColor():
    White = QtGui.QColor(255, 255, 255)
    Black = QtGui.QColor(0, 0, 0)
    Red = QtGui.QColor(255, 0, 0)
    Green = QtGui.QColor(0, 255, 0)
    Blue = QtGui.QColor(0, 0, 255)
    Yellow = QtGui.QColor(255, 255, 0)
    Cyan = QtGui.QColor(0, 255, 255)
    Magenta = QtGui.QColor(255, 0, 255)
    Orange = QtGui.QColor(255, 128, 0)
    Brown = QtGui.QColor(128, 64, 0)
    Purple = QtGui.QColor(128, 0, 128)
    Pink = QtGui.QColor(255, 192, 203)


map_color = {ObjectType.Car: MyColor.Green,
             ObjectType.Truck: MyColor.Yellow,
             ObjectType.Motorcycle: MyColor.Blue,
             ObjectType.Bicycle: MyColor.White,
             ObjectType.Pedestrian: MyColor.Cyan,
             ObjectType.Animal: MyColor.Magenta,
             ObjectType.Hazard: MyColor.Red,
             ObjectType.Unknown: MyColor.Brown,
             ObjectType.Overdrivable: MyColor.Purple,
             ObjectType.Underdrivable: MyColor.Pink}


map_hight = {ObjectType.Car: 2,
             ObjectType.Truck: 4,
             ObjectType.Motorcycle: 1,
             ObjectType.Bicycle: 1,
             ObjectType.Pedestrian: 1,
             ObjectType.Animal: 0.5,
             ObjectType.Hazard: 0.3,
             ObjectType.Unknown: 1,
             ObjectType.Overdrivable: 1,
             ObjectType.Underdrivable: 1}


class BaseObject:
    def __init__(self, length, width, x, y, z, _type):
        self.type = ObjectType(_type)
        if map_color.has_key(self.type):
            self.color = map_color[self.type]
        else:
            self.color = MyColor.White

        if map_hight.has_key(self.type):
            self.hight = map_hight[self.type]
        else:
            self.hight = 0

        self.length = length
        self.width = width

        # self.posn = (-y, x + width, z)
        self.posn = (-y, x , z)


class MyCuboid(BaseObject):
    def __init__(self, length, width, x, y, z, _type, _id, _absV_x, _absV_y, _stMovement=0, _probability=0):
        super(MyCuboid, self).__init__(length, width, x, y, z, _type)
        self.id = _id
        self.stMovement = _stMovement
        self.probability = _probability
        self.absV_x = _absV_x
        self.absV_y = _absV_y

    def setHight(self, hight):
        self.height = hight


class My_cv2_Color():
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Red = (0, 0, 255)
    Green = (0, 255, 0)
    Blue = (255, 0, 0)
    Yellow = (0, 255, 255)
    Cyan = ( 255, 255, 0)
    Magenta = (255, 0, 255)
    Orange = (0, 128, 255)


class obj_shape:
    def __init__(self):
        self.color = My_cv2_Color.White
        self.text = ''
        self.pen_size = 2
        self.font_size = 1

    def set_color(self, color):
        self.color = color

    def set_text(self, text):
        self.text = text

    def set_pen_size(self, pen_size):
        self.pen_size = pen_size

    def set_font_size(self, font_size):
        self.font_size = font_size


class Box_2D(obj_shape):
    def __init__(self, x, y, length, width):
        super(Box_2D, self).__init__()
        self.x = int(x)
        self.y = int(y)
        self.length = int(length)
        self.width = int(width)

    def draw_to_pic(self, pic):
        cv2.rectangle(pic, (self.x, self.y), (self.x + self.length, self.y + self.width), self.color, self.pen_size)  # 画面，左上角坐标，右下角坐标，RGB颜色，厚度
        cv2.putText(pic, self.text, (self.x, self.y - 10), cv2.FONT_HERSHEY_PLAIN, self.font_size, self.color, self.pen_size)  # 画面，文本内容，位置


        # # b_box 左上角坐标
        # ptLeftTop = np.array([self.x, self.y])
        # # 文本框左上角坐标
        # textleftop = []
        # # b_box 右下角坐标
        # ptRightBottom = np.array([self.x + self.length, self.y + self.width])
        # # 画 b_box
        # cv2.rectangle(pic, tuple(ptLeftTop), tuple(ptRightBottom), self.color, self.pen_size)
        # # 获取文字区域框大小
        # t_size = cv2.getTextSize(self.text, self.font_size, cv2.FONT_HERSHEY_PLAIN, self.pen_size)[0]
        # # 获取 文字区域右下角坐标
        # textlbottom = ptLeftTop + np.array(list(t_size))
        # # 绘制文字区域矩形框
        # cv2.rectangle(pic, tuple(ptLeftTop), tuple(textlbottom), self.color, -1)
        # # 计算文字起始位置偏移
        # ptLeftTop[1] = ptLeftTop[1] + (t_size[1] / 2 + 4)
        # # 绘字
        # de_color = (255-self.color[0],255-self.color[1],255-self.color[2])
        # cv2.putText(pic, self.text, tuple(ptLeftTop), cv2.FONT_HERSHEY_PLAIN, 2, de_color, self.pen_size)


class Box_3D(obj_shape):

    #
    #     3-----2
    # 0---|--1  |
    # |   7--|--6
    # 4------5

    def __init__(self, point_list):
        super(Box_3D, self).__init__()
        self.point_list = point_list
        # self.trans_pos2int()

    def trans_pos2int(self):
        print("need to trans pt position to int !!")

    def draw_to_pic(self, pic):
        # 画面，左上角坐标，右下角坐标，RGB颜色，厚度
        cv2.line(pic, self.point_list[0], self.point_list[1], self.color, self.pen_size)
        cv2.line(pic, self.point_list[1], self.point_list[2], self.color, self.pen_size)
        cv2.line(pic, self.point_list[2], self.point_list[3], self.color, self.pen_size)
        cv2.line(pic, self.point_list[3], self.point_list[0], self.color, self.pen_size)
        cv2.line(pic, self.point_list[4], self.point_list[5], self.color, self.pen_size)
        cv2.line(pic, self.point_list[5], self.point_list[6], self.color, self.pen_size)
        cv2.line(pic, self.point_list[6], self.point_list[7], self.color, self.pen_size)
        cv2.line(pic, self.point_list[7], self.point_list[4], self.color, self.pen_size)
        cv2.line(pic, self.point_list[0], self.point_list[4], self.color, self.pen_size)
        cv2.line(pic, self.point_list[1], self.point_list[5], self.color, self.pen_size)
        cv2.line(pic, self.point_list[2], self.point_list[6], self.color, self.pen_size)
        cv2.line(pic, self.point_list[3], self.point_list[7], self.color, self.pen_size)
        # # 获取文字区域框大小
        # t_size = cv2.getTextSize(self.text, self.font_size, cv2.FONT_HERSHEY_PLAIN, self.pen_size)[0]
        # # 获取 文字区域右下角坐标
        # textlbottom = self.point_list[0] + np.array(list(t_size))
        # # 绘制文字区域矩形框
        # cv2.rectangle(pic, self.point_list[0], textlbottom, self.color, -1)
        # # 计算文字起始位置偏移
        # ptLeftTop = self.point_list[0] + np.array(list(t_size))
        # # 绘字
        # cv2.putText(pic, self.text, ptLeftTop, cv2.FONT_HERSHEY_PLAIN, self.font_size, self.color, self.pen_size)


        cv2.putText(pic, self.text, (self.point_list[0][0], self.point_list[0][1]), cv2.FONT_HERSHEY_PLAIN, self.font_size, self.color, self.pen_size)


class Lane_Type():
    Solid = 0,
    Dashed = 1,
    Road_edge = 2


class Lane(obj_shape):
    def __init__(self, point_list):
        super(Lane, self).__init__()
        self.point_list = point_list
        self.color = My_cv2_Color.White
        self.pen_size = 3
        self.type = Lane_Type.Solid

    def set_type(self, type):
        self.type = type

        if self.type == Lane_Type.Solid:
            self.color = My_cv2_Color.White
        elif self.type == Lane_Type.Dashed:
            self.color = My_cv2_Color.Green
        elif self.type == Lane_Type.Road_edge:
            self.color = My_cv2_Color.Orange

    def draw_to_pic(self, pic):
        print('lane contr is:',len(self.point_list))
        for i in range(len(self.point_list)-1):
            cv2.line(pic, self.point_list[i], self.point_list[i+1], self.color, self.pen_size)


class Text_Lable:
    def __init__(self, x, y, text, color=My_cv2_Color.White, font_size=1):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size



# ifDll = CDLL('./fit_1.dll')
# resType = ctypes.c_float * 3
#
#
# class RoadLane:
#     def __init__(self, x, y, z, rcs, ptNr):
#         # floatArrType = ctypes.c_float * ptNr
#         x1 = (ctypes.c_float * ptNr)(*x)
#         y1 = (ctypes.c_float * ptNr)(*y)
#         z1 = (ctypes.c_float * ptNr)(*z)
#         rcs1 = (ctypes.c_float * ptNr)(*rcs)
#         t0=time.time()
#         ifDll.get_guardtral(x1, y1, z1, rcs1, ptNr)
#         t1=time.time()
#         print("*********************time:",t1-t0)
#         print(len(x),len(y),len(z),len(rcs))
#         le_coef = resType.in_dll(ifDll, "le_coef")
#         ri_coef = resType.in_dll(ifDll, "ri_coef")
#
#         self.le_coef = list(le_coef)
#         self.ri_coef = list(ri_coef)
