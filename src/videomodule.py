import os
import numpy as np
import auditok
from pydub import AudioSegment # do stuff to audio in an easy way
import speech_recognition as sr
from moviepy.editor import *
import cv2 as cv
import ffmpeg

def fileIsExisted(file_name:str, file_dir:str):
    path = file_dir
    if os.path.exists(file_dir+file_name):
        return True
    
    return False

# convert video format via FFmpeg
stream_name = input('Enter stream name: ') # change your file here
stream_dir =  "/home/ball45/Videos/" # change your file here
stream_pos = stream_dir + stream_name
if not fileIsExisted(stream_name+'.wav', stream_dir):
    os.system('ffmpeg -i \'' + stream_pos + '.mp4\' \'' + stream_pos + '.wav\'')


# 測試靜音 ----------------------------------
# numpy.zeros(shape, dtype=float, order='C', *, like=None)
record_start = np.zeros(1000)
record_end = np.zeros(1000)
duration = np.zeros(1000)
speech = np.zeros(1000)
num = 0
ins=[]

# Pydub does things in milliseconds
sound = AudioSegment.from_file(stream_pos+'.wav', format="wav") 
# returns generator of AudioRegion objects
audio_regions = auditok.split(
    stream_name + 'wav',
    min_dur=0.2,         # minimum duration of a valid audio event in seconds
    max_dur=100,         # maximum duration of an event
    max_silence=2,       # maximum duration of tolerated continuous silence within an event
    energy_threshold=50  # threshold of detection
)

for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
    speech[i] = record_end[i] - record_start[i]
    print("Speech  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i,r=r), "Duration : ", speech[i])
    num = num+1

for j in range(num-1):
    #evaluate silence section length
    duration[j] = record_start[j+1] - record_end[j]
    print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ', duration[j])

    #if there are two continuous silence sections >2.5 
    if duration[j-1] > 2.5 and duration[j] > 1.9 and speech[j] < 5.0:
        print("instruction : ", round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
        a=int(record_start[j])
        b=int(record_end[j])+1
        #print(a,b,type(a))
        instruction = sound[a*1000:b*1000]
        filename=instruction.export("media/instruction.wav",format="wav")
# 辨識是否為語音指令“剪接” ---------------------------
        r = sr.Recognizer()

        with sr.AudioFile("media/instruction.wav") as source:
            audio = r.record(source)

        try:
            s = r.recognize_google(audio_data=audio, key=None,language="zh-TW", show_all=True)  # , show_all=True
            if "剪接" in str(s):
                print("Instruction : 剪接")
                front = int(record_end[j-1])
                if (front-10) < 0 :
                    ex=0
                else :
                    ex=front-10
                ins.append(int(record_end[j-1]))
                #ins.append(int(record_end[j-1]))
                print(ins)
            else:
                print('pass')

        except r.UnknowValueError:
            Text = "無法翻譯"
        except sr.Requesterror as e:
            Text = "無法翻譯{0}".format(e)

        # 偵測重複 ----------------------------------
        clip = VideoFileClip(inputfile)
        count = 0
        fps = 30
        sum = 0
        summ = 0
        new_frame = []

        #轉灰階
        for frames in clip.iter_frames():
            #print(frames.shape)
            gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
            #cv.imshow("gray", gray) #播放灰階影片
            #print(gray.shape)
            new_frame.append(gray)
            count += 1
            key = cv.waitKey(1)
            if key == ord("q"):
                break

        min = 1000000
        # 比較第t秒和第cutpoint秒的frames，一秒鐘有30個frame(fps=30)
        for cutpoint in range(int(record_start[j+1]),int(record_start[j+1])+5) :
            for t in range(ex,front):
                print(ex,front)
                for k in range(fps+60):
                    for i in np.square(new_frame[t*fps+k] - new_frame[cutpoint*fps+k]):
                        sum = sum + i
                for j in sum :
                    summ = summ + j   
                print('t : ', t, ' - ',cutpoint,' =', summ, '\n')
                if min>summ:
                    t1=t
                    t2=cutpoint
                    min=summ   
                sum = 0
                summ = 0
        #輸出t1和t2最相近
        print (t1,t2,min)