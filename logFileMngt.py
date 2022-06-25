# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
from PyQt5 import QtCore
import time
import protocol
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

    def getTimeStampByLineNr(self,lineNr):
        timestamp_s = 0
        if lineNr >=0 and lineNr <= self.log_file_size -1:
            pclLine = 0
            objLine = 0
            data = 0

            pclLine, objLine = self.get_data_bytes(lineNr)
            if pclLine:
                data = protocol.ARS548_DetectionList(pclLine)
                timestamp_s = data.getTimeStamp_s()
            if objLine:
                data = protocol.ARS548_ObjectList(objLine)
                timestamp_s = data.getTimeStamp_s()

            return timestamp_s

        else:
            return 0

    def getCurrPic(self):
        return self.logFileFolderPath + '/' + self.strNameAffixes + str(self.currPicFileNr) + '.jpg'

    def getNextPic(self):
        self.currPicFileNr += 1
        return self.getCurrPic()

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

    def get_fileLine_by_LineNr(self,lineNr):
        if lineNr >= 0 and lineNr <= self.log_file_size - 1:
            return self.fileLines[lineNr]

    def next_line(self):
        if self.currLineNr < self.log_file_size:
            self.currLineNr += 1

    def get_data_bytes(self, lineNr):
        pcl_dataBytes = 0
        obj_dataBytes = 0

        bytes_data = bytes.fromhex(self.get_fileLine_by_LineNr(lineNr))
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

    def set_Progress(self):
        pass

    def parse_obj_list(self,data_bytes):
        obj_buf = data_bytes[16:9385 + 16]
        obj_list = protocol.ARS548_ObjectList(obj_buf)
        return obj_list

    def parse_pcl(self,bytes_data):
        buf = bytes_data[16:35305 + 16]
        dList = protocol.ARS548_DetectionList(buf)
        return dList



