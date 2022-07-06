# encoding:utf-8

import cv2
import numpy as np

pic_shape = (480, 640, 3)
image = np.zeros(pic_shape, dtype=np.uint8)  # 黑色画布
GrayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

x, y, w, h = cv2.boundingRect(GrayImage)

draw_1 = cv2.rectangle(GrayImage, (10, 20), (x + w, y + h), (0, 255, 0), 2)
# 参数：pt1,对角坐标１, pt2:对角坐标２
# 注意这里根据两个点pt1,pt2,确定了对角线的位置，进而确定了矩形的位置
# The function cv::rectangle draws a rectangle outline or a filled rectangle whose two opposite corners are pt1 and pt2.
# draw_0 = cv2.rectangle(image, (2 * w, 2 * h), (3 * w, 3 * h))



cv2.imshow("draw_0", draw_1)  # 显示画过矩形框的图片
cv2.waitKey(0)
cv2.destroyWindow("draw_0")