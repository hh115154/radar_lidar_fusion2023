# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/7/14 16:15
# @File     : hex_log_file.py
# @Project  : radar_fusion

import my_util
import bisect as bs
timeStampStr_len = 13
import datetime


class Parse_Majority_Log_File():
    def __init__(self, log_file_name):
        self.log_file_name = log_file_name
        self.log_file = open(log_file_name, 'r')
        self.fileLines = self.log_file.readlines()
        if len(self.fileLines) == 0:
            print('log file is empty')
            return

        self.curr_line_nr = 0

        self.timestamp_map_framedata = {}
        for line in self.fileLines:
            ts = line[0:timeStampStr_len]
            self.timestamp_map_framedata[my_util.get_timestamp_from_str(ts)] = line[timeStampStr_len + 1:]

        self.timestamp_list = list(self.timestamp_map_framedata.keys())
        self.curr_time_stamp = self.timestamp_list[0]

        self.log_file_size = len(self.timestamp_map_framedata)
        self.ts_list = list(self.timestamp_map_framedata.keys())
        self.delta_t = self.ts_list[3] - self.ts_list[2]
        self.delta_t = self.delta_t - self.delta_t % datetime.timedelta(microseconds=10000)
        print('hi')

    def bin_search_nearest_frame(self, time_stamp):
        i = bs.bisect_left(self.ts_list, time_stamp)
        return self.ts_list[i]

    def get_frame_by_timestamp(self, time_stamp):
        ts = self.bin_search_nearest_frame(time_stamp)
        return self.timestamp_map_framedata[ts]

    def get_curr_frame(self):
        ts = self.get_timestamp_by_line_num(self.curr_line_nr)
        return self.timestamp_map_framedata[ts]

    def next_frame(self):
        self.curr_line_nr += 1
        self.curr_line_nr %= self.log_file_size
        # ++1 until match the valid line of data

    def get_timestamp_by_line_num(self, line_num):
        return self.timestamp_list[line_num]


class Parse_Extra_Log_File(Parse_Majority_Log_File):
    def __init__(self, log_file_name):
        super(Parse_Extra_Log_File, self).__init__(log_file_name)


lf = Parse_Majority_Log_File('C:/Apps/radar_fusion/myLogFolder/Record_2022-07-15_11-52-02/Record_2022-07-15_11-52-02.zmq.j3radar_fusion.hex')





