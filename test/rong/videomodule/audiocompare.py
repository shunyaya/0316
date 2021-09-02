#!/usr/bin/env python
#! --*-- coding:utf-8 --*--
import cv2



video = cv2.VideoCapture("media/IMG_9588.MOV")
fps = video.get(cv2.CAP_PROP_FPS)
fps = round(fps,)  
print(fps)     
video.release()


