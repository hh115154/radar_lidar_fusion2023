# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 19:17
# @File     : ConfigConstantData.py
# @Project  : radar_fusion

radar4D_548 = 0
J3C = 1

dataSource = J3C

#ip
J3C_socket_if = 'tcp://10.13.1.12:6060'


#protocol
ObjListByteNr = 9401
PclByteNr = 35336

#time
timer_readlogfile_ms = 50# 實際應該是50

# log file and pic file
picture_saved_path = '/myLogFolder/'
logFile_head_affix = 'Record_'
logfile_tail_affix = '.someip.ars540.hex'

