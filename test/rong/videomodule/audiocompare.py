#!/usr/bin/env python
#! --*-- coding:utf-8 --*--
import cv2

def cap_fps(major_ver):
    
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        #print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        #print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    
    return(fps)

video = cv2.VideoCapture("media/tetest.mp4")

# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(cap_fps(major_ver)  )     
video.release()


