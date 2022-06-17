# from testRecordVidio import inpFps,outpFps

import cv2
vidioFileName = "video.mp4"

cap = cv2.VideoCapture(vidioFileName)


bPlaying = False

if cap.isOpened():
	bPlaying = True
else:
	print("视频打开失败")


# 2.循环读取图片
newSize = (640,480) #使用大尺寸窗口播放视频
while cap.isOpened():
	fps = int(cap.get(cv2.CAP_PROP_FPS))
	ret, frame = cap.read()
	if ret:
		framePlay = cv2.resize(frame, newSize)
		cv2.imshow(vidioFileName, framePlay)
	else:
		print("视频播放完成！")
		break

	# 退出播放
	key = cv2.waitKey(6*fps*6) #摄像头原始Fps * 压缩比
	if key == 27:  # 按键esc
		break




# 释放视频流

cap.release()

# 关闭所有窗口

cv2.destroyAllWindows()
