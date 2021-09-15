import os
import numpy as np
import auditok
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import *
import cv2 as cv

def Input(sourcefile):
    source_file = sourcefile
    slash_pos = source_file.rfind('/')
    dot_pos = source_file.rfind('.')
    source_path, source_name = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos]
    wav_file = source_path + source_name + '.wav'
    out_file = source_path + source_name + '_out.mp4'

    if not os.path.exists(wav_file):
        os.system("ffmpeg -i "+source_file+" "+source_path + source_name + '.wav')
    
    return source_file, wav_file, out_file

#轉灰階
def GrayScalar(sourcefile):
    clip = VideoFileClip(sourcefile)
    gray_scalar = []
    for frames in clip.iter_frames():
        gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
        gray_scalar.append(gray)
        key = cv.waitKey(1)
        if key == ord("q"):
            break

    # frame size
    print('number of frames: ', len(gray_scalar))
    print('frame size : W =', len(gray_scalar[0]), 'H =', len(gray_scalar[0]))
    return gray_scalar

# 找出fps
def DetectFps(source_file):
    clip = cv.VideoCapture(source_file)
    fps = clip.get(cv.CAP_PROP_FPS)
    fps = round(fps,)       
    clip.release()
    return fps

# 辨識是否為語音指令“剪接”
def RecIns(wavfile,ins_start):
    r = sr.Recognizer()
    instruction = sr.AudioFile(wavfile)
    with instruction as source:
        audio = r.record(source, offset = ins_start, duration = 5)
    try:
        ins = r.recognize_google(audio_data=audio, key=None,language="zh-TW", show_all=True)  # show_all=True
    except sr.UnknownValueError:
        ins = "無法翻譯"
    except sr.RequestError as e:
        ins = "無法翻譯{0}".format(e)
    
    return str(ins)

#測試平方
def CutPoint(gray_scalar, before_ins_end, after_ins_start, fps):   
    #before_ins_end   指令前的結束時間
    #before_ins_start 指令前的起始時間
    #after_ins_start  指令後的起始時間
    
    min = 100000000000
    # 抓影片前5秒進行辨識
    if before_ins_end < 5 :
        before_ins_start=0 
    else :
        before_ins_start = before_ins_end-5    
        
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
    
def main(sourcefile):
    file = Input(sourcefile) 
    gray_scalar =  GrayScalar(file[0]) 
    fps = DetectFps(file[0]) 
    
    # 測試靜音 
    wavfile = file[1]
    audio_regions = auditok.split(
        wavfile,
        min_dur=0.2,         # minimum duration of a valid audio event in seconds
        max_dur=100,         # maximum duration of an event
        max_silence=2,       # maximum duration of tolerated continuous silence within an event
        energy_threshold=50  # threshold of detection
    )
    record_start = np.zeros(1000)
    record_end = np.zeros(1000)
    speech_duration = np.zeros(1000)
    silence_duration = np.zeros(1000)
    num = 0

    for i, r in enumerate(audio_regions):
        record_start[i] = r.meta.start
        record_end[i] = r.meta.end
        speech_duration[i] = record_end[i] - record_start[i]
        num = num+1
    
    for j in range(num-1):
        silence_duration[j] = record_start[j+1] - record_end[j]
        #print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ', silence_duration[j])
        # if there are two continuous silence sections >2.5 
        if silence_duration[j-1] > 1.4 and silence_duration[j] > 1.4 and speech_duration[j] < 5.0:
            #print("instruction : ", round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
            if "剪接" in RecIns(file[1],round(record_start[j], 3)):
                print("Instruction: 剪接") 
                CutPoint(gray_scalar, int(record_end[j-1]), round(record_start[j+1], 3), fps)
     
if __name__ == "__main__" :
    main("media/tetest.mp4")






