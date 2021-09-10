from moviepy.editor import *
import numpy as np
import cv2 as cv


clip = VideoFileClip("media/tetest.mp4")
fps = 20
gray_scalar = []

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

gray_scalar_array = np.array(gray_scalar)
# frame size
#gray_scalar.reshape = np
print(gray_scalar_array.shape)
print('number of frames: ', len(gray_scalar))
print('frame size : W =', len(gray[0]), 'H =', len(gray_scalar[0]))

#測試平方
min = 100000
for i in range(10*fps):
    before_ins = []
    after_ins = []
    for j in range(1):  
    before_ins.append(gray_scalar[before_ins_start*fps+i+j])
    after_ins.append(gray_scalar[round(after_ins_start*fps)+j])
                    
    before_ins_array = np.array(before_ins)
    after_ins_array = np.array(after_ins)
                    
    d = (before_ins_array-after_ins_array)**2
                    
    if min > d.sum():
        tmin = (before_ins_start*fps+i)/fps 
         min = d.sum()
    print('t : ', (before_ins_start*fps+i+j)/fps,' ', d.sum())          
    #輸出t1和t2最相近
    print(tmin, min)
    



