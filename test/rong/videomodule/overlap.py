#from moviepy.editor import VideoFileClip
from moviepy.editor import *
import numpy as np
import cv2 as cv


clip = VideoFileClip("media/IMG_9589.MOV")
fps = 30
sum = 0
summ = 0
gray_scalar = []
add = 0

#轉灰階
for frames in clip.iter_frames():
    #print(frames.shape)
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray) #播放灰階影片
    #print(gray.shape)
    gray_scalar.append(gray)
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# frame size
print('number of frames: ', len(gray_scalar))
print('frame size : W =', len(gray[0]), 'H =', len(gray_scalar[0]))

#測試加減、平方有沒有錯
#print('new_frame[0] : ', new_frame[0])
#print('new_frame[270] : ', new_frame[270])

#測試減法
#xx=new_frame[270] - new_frame[0]
#print(xx)

#測試平方
before_ins = gray_scalar[120]
after_ins = gray_scalar[1200]

d = (before_ins-after_ins)**2
d.sum()
print(d.sum())


min = 1000000
# 比較第t秒和第cutpoint秒的frames，一秒鐘有30個frame(fps=30)
for cutpoint in range(40,42) :
    for t in range(4,14):
        for sec in range(0,2) :
            if add == 1 :
                tt=t+0.5
                time=t*30+15
                add = 0
            else :
                add=1
                tt=t
                time = t*30
            for k in range(fps+120):
                for i in np.square(gray_scalar[time+k] - gray_scalar[cutpoint*30+k]):
                    sum = sum + i
            for j in sum :
                summ = summ + j   
            print('t : ', tt, ' - ',cutpoint,' =', summ, '\n')
            if min>summ:
                t1=tt
                t2=cutpoint
                min=summ   
            sum = 0
            summ = 0
#輸出t1和t2最相近
print (t1,t2,min)

