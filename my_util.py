# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/7/8 17:45
# @File     : my_util.py
# @Project  : radar_fusion

from datetime import datetime
from string import Template



time_stamp_format_str = '%H-%M-%S.%f'#'%H:%M:%S.%f'

def get_timestamp_str():
    return datetime.now().strftime(time_stamp_format_str)[:-3]

def get_timestamp_from_str(str):
    return datetime.strptime(str, time_stamp_format_str)

# def get_timestamp_from_fmt_str(str, fmt):
#     return datetime.strptime(str, fmt)

class DeltaTemplate(Template):
    delimiter ="%"

def strfdelta(tdelta, fmt='%H:%M:%S'):
    d = {}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


