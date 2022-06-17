

# -*-coding:utf-8-*-

import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)#打开摄像头

#采样精度不可调？
inpSize = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
		int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

inpFps = int(cap.get(cv2.CAP_PROP_FPS)) #摄像头原始帧率30


if inpFps< 30:
	inpFps = 30


#制定保存格式，注意要与保存文件的后缀匹配
# fourcc = cv2.VideoWriter_fourcc('X', '2', '6', '4')
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')


outpSize = (400, 300) #保存视频的精度
outpFps = int(5) #压缩到1/6
videoWriter = cv2.VideoWriter('video.mp4', fourcc, outpFps, outpSize) #初始化writer参数

ret = True
frameNr = 0
while ret:
	ret, frame = cap.read()
	frameNr = frameNr + 1
	# 展示一帧
	cv2.imshow("captureOrg", frame) #原始采样数据
	cv2.waitKey(1)
	if frameNr % int(inpFps/outpFps) == 0:
		outpFrame = cv2.resize(frame, outpSize) #压缩视频精度
		cv2.imshow("captureZipped", outpFrame) #另起窗口展示压缩后的视频
		videoWriter.write(outpFrame) #保存压缩后的视频



cap.release()

cv2.destroyAllWindows()
