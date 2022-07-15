# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 19:17
# @File     : ConfigConstantData.py
# @Project  : radar_fusion

radar4D_548 = 0
J3System = 1

MachineType = J3System

#ip
J3C_socket_if = 'tcp://10.13.1.12:6060'
J3A_socket_if = 'tcp://10.13.1.10:5560'


#protocol
ObjListByteNr = 9401
PclByteNr = 35336

#time
timer_readlogfile_ms = 50# 實際應該是50
timer_online_sensor_show_ms = 100#
timer_online_sensor_show_and_log_ms = 200#
timer_online_pic_show_ms = 120

# log file and pic file
picture_saved_path = '/myLogFolder/'
logFile_head_affix = 'Record_'
logfile_tail_affix_4D548 = '.someip.ars540.hex'
logfile_tail_affix_J3Camera = '.zmq.j3camera.hex'
logfile_tail_affix_J3Fusion = '.zmq.j3radar_fusion.hex'
mark_line_head = '#hh# @'


#pic info
camera_id = 1 #0:laptop ; 1: external camera
pic_width = 3840
pic_height = 2160




