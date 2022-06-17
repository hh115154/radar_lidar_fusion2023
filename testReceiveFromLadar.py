from socket import *
import struct

port = 42102
pcIp = '10.13.1.199'
pcAddr = (pcIp, port)

group_ip = '224.0.2.2'

if __name__ == '__main__':
    #建立udp socket
    mySocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    # mySocket = socket(AF_INET, SOCK_STREAM)
    #绑定 端口号，端口号不能改
    mySocket.bind(pcAddr)

    #加入组播组
    # mreq = struct.pack("=4sl", inet_aton(group_ip), INADDR_ANY)
    # mySocket.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)

    while True:
        try:
            # recv_message, client = mySocket.recvfrom(2048)
            # print("recv_message len of: ",len(recv_message),"data is :", recv_message)
            cmd_res_size = mySocket.recv(2048)
            print("cmd_res_size len of: ",len(cmd_res_size))
            # print(cmd_res_size)
        except Exception as e:
            print(e)


