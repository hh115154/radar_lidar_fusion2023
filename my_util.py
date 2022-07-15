# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/7/8 17:45
# @File     : my_util.py
# @Project  : radar_fusion

from datetime import datetime


time_stamp_format_str = '%H-%M-%S.%f'#'%H:%M:%S.%f'

def get_timestamp_str():
    return datetime.now().strftime(time_stamp_format_str)[:-3]

def get_timestamp_from_str(str):
    return datetime.strptime(str, time_stamp_format_str)
