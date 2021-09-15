from moviepy.editor import *
import numpy as np
import cv2 as cv

#轉灰階
def GrayScalar(clip):
    gray_scalar = []
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
    print('frame size : W =', len(gray_scalar[0]), 'H =', len(gray_scalar[0]))
    return gray_scalar

#測試平方
def CutPoint(gray_scalar):
    min = 100000000000
    fps = 20
                
    # 抓影片前5秒進行辨識
    before_ins_end = int(7)      #指令前的結束時間
    if (before_ins_end-5) < 0 :
        before_ins_start=0
    else :
        before_ins_start = before_ins_end-5    #指令前的起始時間
        
    after_ins_start = float(14.5) # 指令後的起始時間

    for i in range(5*fps):
        before_ins = gray_scalar[before_ins_start*fps+i]
        after_ins = gray_scalar[round(after_ins_start*fps)]
        
        d = (before_ins-after_ins)**2
        
        if min > d.sum():
            cutpoint = (before_ins_start*fps+i)/fps 
            min = d.sum()
        #print('t : ', round(before_ins_start*fps+i+j, 1)/fps,' ', d.sum())          
    #輸出最相近
    print(cutpoint, min)
    
if __name__ == "__main__" :
    clip = VideoFileClip("media/tetest.mp4")
    CutPoint(GrayScalar(clip))




