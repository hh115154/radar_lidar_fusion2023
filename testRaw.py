import cv2
import numpy as np


types = [8394756,
8393729,
8393730,
8398856,
8454144,
8454144,
16783364,
16782337,
16782338,
16787464
]

for t in types:
    print(bin(t))




def drawline(img,pt1,pt2,color,thickness=1,gap=20):
    dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
    pts= []
    for i in np.arange(0,dist,gap):
        r=i/dist
        x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
        y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
        p = (x,y)
        pts.append(p)


    s=pts[0]
    e=pts[0]
    i=0
    for p in pts:
        s=e
        e=p
        if i%2==1:
            cv2.line(img,s,e,color,thickness)
        i+=1

def drawpoly(img,pts,color,thickness=1):
    s=pts[0]
    e=pts[0]
    pts.append(pts.pop(0))
    for p in pts:
        s=e
        e=p
        drawline(img,s,e,color,thickness)

def drawrect(img,pt1,pt2,color,thickness=1):
    pts = [pt1,(pt2[0],pt1[1]),pt2,(pt1[0],pt2[1])] 
    drawpoly(img,pts,color,thickness)

im = np.zeros((800,800,3),dtype='uint8')
s=(234,222)
e=(500,700)
# drawrect(im,s,e,(0,255,255),1,'dotted')
drawrect(im,s,e,(0,255,255),1)

cv2.imshow('im',im)
cv2.waitKey()   