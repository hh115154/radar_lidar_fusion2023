import cv2
import os


im_dir = r'C:\Users\yangh\Desktop\log'
# fix_str = "Record_2021-12-05_11-31-31_Frame_"
fix_str = "Record_2021-10-14_16-43-39_Frame_"
strtNr = int(7539)

video_dir = r'C:\Users\yangh\Desktop\log1.avi'

fps = 30
num = 859
# num = 18
img_size = (640, 480)
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')

videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)

for i in range(1, num):
	im_name = os.path.join(im_dir, fix_str + str(i + strtNr).zfill(4) + '.jpg')
	frame = cv2.imread(im_name)
	videoWriter.write(frame)
	print(im_name)

videoWriter.release()
print('finish')
