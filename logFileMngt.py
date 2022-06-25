# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
from PyQt5 import QtCore
import os


class RadarLogFileInfo(): # 区分视频文件还是雷达log文件
    def __init__(self, log_file_name):#full path

        self.log_file_full_path = log_file_name

        fileInfo = QtCore.QFileInfo(self.log_file_full_path)
        self.logFileFolderPath = fileInfo.absolutePath()

        self.log_file_name = fileInfo.fileName()
        self.strNameAffixes = self.log_file_name[0:26]
        self.strNameAffixes += '_Frame_'

        file_list = os.listdir(self.logFileFolderPath)
        self.sortedPicFileList = []
        self.currPicFileNr = 0
        self.maxPicFileNr = 0
        self.hasPicFiles = False
        if len(file_list) >1:
            self.hasPicFiles = True
            self.sortPicFileNameAsNum(file_list[1:])

        file = open(self.log_file_full_path, "r")
        self.fileLines = file.readlines()
        self.log_file_size = len(self.fileLines)
        self.currLineNr = 0

    def sortPicFileNameAsNum(self, picFileList):
        numLenMap = {1: [], 2: [], 3: [], 4: [], 5: []}
        for picFile in picFileList:
            numLenMap[len(self.getPicNameNrStr(picFile))].append(picFile)

        for i in range(len(numLenMap)):
            if numLenMap[i+1]:
                self.sortedPicFileList.extend(numLenMap[i+1])
        self.currPicFileNr = self.getPicNameNr(self.sortedPicFileList[0])
        self.maxPicFileNr = self.getPicNameNr(self.sortedPicFileList[-1])



    def getPicNameNr(self,strPicName):
        tmp = strPicName[33:]
        return int(tmp[:-4])

    def getPicNameNrStr(self,strPicName):
        tmp = strPicName[33:]
        return tmp[:-4]

    def getPrograss(self):
        return self.currLineNr/self.log_file_size

    def get_current_line(self):
        if self.currLineNr < self.log_file_size:
            return self.fileLines[self.currLineNr]


    def next_line(self):
        if self.currLineNr < self.log_file_size:
            self.currLineNr += 1

    def get_data_bytes(self):
        pcl_dataBytes = 0
        obj_dataBytes = 0

        bytes_data = bytes.fromhex(self.get_current_line())
        line_len = len(bytes_data)

        if line_len > 10000:
            pcl_dataBytes = bytes_data
            while line_len > 10000:
                pcl_dataBytes = bytes_data
                self.currLineNr += 1
                bytes_data = bytes.fromhex(self.get_current_line())
                line_len = len(bytes_data)
            obj_dataBytes = bytes_data
        else:
            while line_len < 10000:
                self.currLineNr += 1
                pcl_dataBytes = bytes.fromhex(self.get_current_line())
                line_len = len(pcl_dataBytes)
            while line_len > 10000:
                self.currLineNr += 1
                obj_dataBytes = bytes.fromhex(self.get_current_line())
                line_len = len(obj_dataBytes)
        return pcl_dataBytes, obj_dataBytes




