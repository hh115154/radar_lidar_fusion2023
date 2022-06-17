#coding=utf-8

from socket import *
import struct
import protocol
# from procAsamMdf import MdfSignal
import time

# 1. 创建udp套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)
port = 8080
pcIp = '10.0.5.199'
pcAddr = (pcIp, port)
adptrIp = '10.0.5.10'
adptrAddr = (adptrIp,port)

udp_socket.bind(pcAddr)

print("listening to the network...")
if __name__ =='__main__':

    # mySig = MdfSignal()
    frmNr = 0
    # recv_data = udp_socket.recvfrom(dataBufLen)
    while True:
        recv_message, client = udp_socket.recvfrom(1024)
        data = struct.unpack('>44B',recv_message)

        bytes =int.from_bytes(data, byteorder='big').to_bytes(44,byteorder='big')
        appData = protocol.Detection(bytes)
        ti = time.time()
        frmNr+=1
        # mySig.appendNewTimeStampData(appData, ti)

        print(appData)
        if frmNr > 5:
            mySig.export2file('my_first_mdf_file.mf4')
#
# # 2. 准备对方的地址
# # 8080表示目的端口
# dest_addr = ('10.0.5.10', int(8080))# 注意 是元组，ip是字符串，端口是数字
#
# # 3. 从键盘获取数据
# #send_data = input("请输入要发送的数据:")
#
# # 4. 发送数据到指定的电脑上的指定程序中
#
# udp_socket.sendto(b'\x22\x33\x44\x55', dest_addr)
# #udp_socket.sendto(send_data.encode('utf-8'), dest_addr)
#
#
#
# # 5. 关闭套接字
# udp_socket.close()