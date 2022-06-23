import time
from enum import Enum
from PyQt5 import QtGui
from ctypes import *
import ctypes

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
        self.color = map_color[self.type]
        self.height = map_hight[self.type]

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
