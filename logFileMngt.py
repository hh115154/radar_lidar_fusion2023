# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
from PyQt5 import QtCore
import time
import os
import protocol
import ConfigConstantData



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
        self.firstPicFileNr = 0
        self.currPicFileNr = 0
        self.maxPicFileNr = 0
        self.hasPicFiles = False
        if len(file_list) >1:
            self.hasPicFiles = True
            self.sortPicFileNameAsNum(file_list[1:])

        self.picFilesCount = len(file_list)-1
        file = open(self.log_file_full_path, "r")
        self.fileLines = file.readlines()
        self.log_file_size = len(self.fileLines)
        self.currLineNr = 0

    def is_end(self):
        return self.currLineNr >= self.log_file_size

    def getTimeStampByLineNr(self,lineNr):
        timestamp_s = 0
        data = 0
        if lineNr >=0 and lineNr <= self.log_file_size -1:
            data = self.get_data_bytes(lineNr)
            if len(data) == ConfigConstantData.PclByteNr:
                data = self.parse_pcl(data)
                timestamp_s = data.getTimeStamp_s()
            elif len(data) == ConfigConstantData.ObjListByteNr:
                data = self.parse_obj_list(data)
                timestamp_s = data.getTimeStamp_s()

            return timestamp_s

        else:
            return 0

    def getCurrPic(self):
        return self.logFileFolderPath + '/' + self.strNameAffixes + str(self.currPicFileNr) + '.jpg'

    def getNextPic(self):
        self.currPicFileNr += 1
        self.currLineNr %= self.maxPicFileNr
        return self.getCurrPic()

    def sortPicFileNameAsNum(self, picFileList):
        numLenMap = {1: [], 2: [], 3: [], 4: [], 5: []}
        for picFile in picFileList:
            try:
                numLenMap[len(self.getPicNameNrStr(picFile))].append(picFile)
            except:
                print('请不要修改原始log文件夹，或增加内容')
        for i in range(len(numLenMap)):
            if numLenMap[i+1]:
                self.sortedPicFileList.extend(numLenMap[i+1])
        self.firstPicFileNr = self.getPicNameNr(self.sortedPicFileList[0])
        self.currPicFileNr = self.firstPicFileNr
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
        else:
            return self.fileLines[-1]

    def get_fileLine_by_LineNr(self,lineNr):
        return self.fileLines[lineNr]

    def goback_oneStep(self):
        if self.currLineNr >= 4:
            self.currLineNr -= 4
        else:
            self.currLineNr = 0

    def next_line(self):
        self.currLineNr += 1
        self.currLineNr %= self.log_file_size

    def get_data_bytes(self, lineNr):
        try:
            bytes_data = bytes.fromhex(self.get_fileLine_by_LineNr(lineNr))
        except Exception as e:
            print(e)
        return bytes_data

    def set_Progress(self, lineNr):
        self.currLineNr = lineNr
        self.currPicFileNr = self.firstPicFileNr + int(self.maxPicFileNr * self.currLineNr/self.log_file_size)

    def parse_obj_list(self,data_bytes):
        obj_buf = data_bytes[16:9385 + 16]
        obj_list = protocol.ARS548_ObjectList(obj_buf)
        return obj_list

    def parse_pcl(self,bytes_data):
        buf = bytes_data[16:35305 + 16]
        dList = protocol.ARS548_DetectionList(buf)
        return dList



