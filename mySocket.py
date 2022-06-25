# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
import socket
from socket import *
import struct


class MyUdpSocket:
	def __init__(self):
		self.pcPort = 42102
		self.pcIp ='' # 本地ip，不用指明
		self.group_ip = '224.0.2.2'

		self.pcAddr = (self.pcIp, self.pcPort)
		# self.adptrPort = int(8080)
		self.adptrIp = '10.13.1.11'
		# self.adptrAddr = (self.adptrIp, self.adptrPort)
		self.rcvBufLen = 65536
		self.isConnected = False

		try:
			self.udp_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
			self.udp_socket.bind(('',self.pcPort))

			# 加入组播组
			mreq = struct.pack("=4sl", inet_aton(self.group_ip), INADDR_ANY)
			self.udp_socket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)


			print("listening to the network...")
			self.isConnected = True
		except Exception as e:
			print("no ethernet device")
			print(e)
			self.isConnected = False

	def __del__(self):
		self.udp_socket.close()





