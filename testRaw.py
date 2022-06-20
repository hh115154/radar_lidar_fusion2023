import numpy as np
import imageio

rawfile = np.fromfile('0.raw', dtype=np.float32)  # 以float32读图片
print(rawfile.shape)
# rawfile.shape = (20622,)
print(rawfile.shape)
b = rawfile.astype(np.uint8)  # 变量类型转换，float32转化为int8
print(b.dtype)
imageio.imwrite("0.jpg", b)

import matplotlib.pyplot as pyplot

pyplot.imshow(rawfile)

