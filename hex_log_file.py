# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/7/14 16:15
# @File     : hex_log_file.py
# @Project  : radar_fusion

import my_util

timeStampStr_len = 13


class Parse_Log_File():
    def __init__(self, log_file_name):
        self.log_file_name = log_file_name
        self.log_file = open(log_file_name, 'r')
        fileLines = self.log_file.readlines()

        self.log_file_lines = {}
        for line in fileLines:
            ts = line[0:timeStampStr_len]
            self.log_file_lines[my_util.get_timestamp_from_str(ts)] = line[timeStampStr_len+1:]
        self.log_file_size = len(self.log_file_lines)

        str = '10:47:46.0708'
        ts1 = my_util.get_timestamp_from_str(str)

        if ts1 in self.log_file_lines:
            print(self.log_file_lines[ts1])
        else:
            print('not found')
        print('hi')


lf = Parse_Log_File('C:/Apps/radar_fusion/myLogFolder/Record_2022-07-14_10-47-43/Record_2022-07-14_10-47-43.zmq.j3radar_fusion.hex')






