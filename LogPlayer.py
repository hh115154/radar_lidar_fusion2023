# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:22
# @File     : LogPlayer.py
# @Project  : radar_fusion

from enum import Enum


class PlayerState(Enum):
    IDLE = 1
    PLAYING = 2
    PAUSE = 3


class LogPlayer():
    def __init__(self):
        self.playSt = PlayerState.IDLE
        self.bOnline = False # online means with Radar/ offline means read log file

