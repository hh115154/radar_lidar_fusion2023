# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/7/14 16:15
# @File     : hex_log_file.py
# @Project  : radar_fusion
import ConfigConstantData
import my_util
import bisect as bs
timeStampStr_len = 12
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
        self.marked_timestamp_list = []

        self.timestamp_map_framedata = {}
        for line in self.fileLines:
            if line.startswith(ConfigConstantData.mark_line_head):
                line = line[len(ConfigConstantData.mark_line_head):]
                marked_ts = line[0:timeStampStr_len]
                self.marked_timestamp_list.append(marked_ts)

            ts = line[0:timeStampStr_len]
            self.timestamp_map_framedata[my_util.get_timestamp_from_str(ts)] = bytes.fromhex(line[timeStampStr_len:])

        self.timestamp_list = list(self.timestamp_map_framedata.keys())

        self.log_file_size = len(self.timestamp_map_framedata)
        self.ts_list = list(self.timestamp_map_framedata.keys())

        self.delta_t_ms = self.get_time_step()

    def get_time_step(self):
        delta_t = self.ts_list[3] - self.ts_list[2]
        delta_t = delta_t - delta_t % datetime.timedelta(microseconds=10000)
        return int(delta_t.microseconds / 1000)

    def bin_search_nearest_frame(self, time_stamp):
        i = bs.bisect_left(self.ts_list, time_stamp)
        return self.ts_list[i]

    def get_frame_by_timestamp(self, time_stamp):
        ts = self.bin_search_nearest_frame(time_stamp)
        return self.timestamp_map_framedata[ts]

    def jump_to_timestamp(self, time_stamp):
        ts = self.bin_search_nearest_frame(time_stamp)
        self.curr_line_nr = self.timestamp_list.index(ts)

    def get_curr_frame(self):
        ts = self.timestamp_list[self.curr_line_nr]
        return self.timestamp_map_framedata[ts]

    def get_progress(self):
        return self.curr_line_nr

    def set_progress(self, _line_nr):
        self.curr_line_nr = _line_nr

    def next_frame(self):
        self.curr_line_nr += 1
        self.curr_line_nr %= self.log_file_size
        # ++1 until match the valid line of data

    def goback_oneStep(self):
        if self.curr_line_nr >= 4:
            self.curr_line_nr -= 4
        else:
            self.curr_line_nr = 0

    def get_curr_timestamp(self):
        return self.timestamp_list[self.curr_line_nr]


class Parse_Extra_Log_File(Parse_Majority_Log_File):
    def __init__(self, log_file_name):
        super(Parse_Extra_Log_File, self).__init__(log_file_name)


# lf = Parse_Majority_Log_File('C:/Apps/radar_fusion/myLogFolder/Record_2022-07-15_11-52-02/Record_2022-07-15_11-52-02.zmq.j3radar_fusion.hex')






