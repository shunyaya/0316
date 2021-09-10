import os
import numpy as np
import auditok
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import *
from moviepy import editor
import cv2 as cv

# mp4 轉成 wav -----------------------------
#inputfile = "media/tainanvlog.mp4"
source_file = "media/IMG_9589.MOV"
slash_pos = source_file.rfind('/')
dot_pos = source_file.rfind('.')
source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
wavfile = source_path + source_name + '.wav'
outfile = source_path + source_name + '_out.mp4'

if not os.path.exists(wavfile):
    os.system("ffmpeg -i "+source_file+" "+source_path + source_name + '.wav')


#轉灰階--------------------------------------
clip = VideoFileClip(source_file)
gray_scalar = []
for frames in clip.iter_frames():
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray) #播放灰階影片
    gray_scalar.append(gray)
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# 找出fps---------------------------------------
clip = cv.VideoCapture(source_file)
fps = clip.get(cv.CAP_PROP_FPS)
fps = round(fps,)       
clip.release()

# 測試靜音 ----------------------------------
# split returns a generator of AudioRegion objects
sound = AudioSegment.from_file(wavfile, format="wav") 
audio_regions = auditok.split(
    wavfile,
    min_dur=0.2,         # minimum duration of a valid audio event in seconds
    max_dur=100,         # maximum duration of an event
    max_silence=2,       # maximum duration of tolerated continuous silence within an event
    energy_threshold=50  # threshold of detection
)

record_start = np.zeros(1000)
record_end = np.zeros(1000)
silence_duration = np.zeros(1000)
speech_duration = np.zeros(1000)
num = 0
cut=1

for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
    num = num+1

for j in range(num-1):
    # evaluate silence section length
    silence_duration[j] = record_start[j+1] - record_end[j]
    print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ', silence_duration[j])

    # if there are two continuous silence sections >2.5 
    if silence_duration[j-1] > 1.4 and silence_duration[j] > 1.4 and speech_duration[j] < 5.0:
        #print("instruction : ", round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
        a=int(record_start[j])
        b=int(record_end[j])+1
        instruction = sound[a*1000:b*1000]
        filename=instruction.export("media/instruction.wav",format="wav")

# 辨識是否為語音指令“剪接” ---------------------------
        r = sr.Recognizer()

        with sr.AudioFile("media/instruction.wav") as source:
            audio = r.record(source)
        try:
            s = r.recognize_google(audio_data=audio, key=None,language="zh-TW", show_all=True)
            if "剪接" in str(s):
                print("Instruction : 剪接")                
# 偵測重複 ----------------------------------
                min = 100000000000
                
                # 抓影片前5秒進行辨識
                before_ins_end = int(record_end[j-1])      #指令前的結束時間
                if (before_ins_end-5) < 0 :
                    before_ins_start=0
                else :
                    before_ins_start = before_ins_end-5    #指令前的起始時間
                  
                after_ins_start = float(record_start[j+1]) # 指令後的起始時間
                
                for i in range(10*fps):
                    before_ins = gray_scalar[before_ins_start*fps+i]
                    after_ins = gray_scalar[round(after_ins_start*fps)]
                    
                    d = (before_ins-after_ins)**2
                    
                    if min > d.sum():
                        cutpoint = (before_ins_start*fps+i)/fps 
                        min = d.sum()
                    #print('t : ', round(before_ins_start*fps+i+j, 1)/fps,' ', d.sum())          
                #輸出最相近
                print(cutpoint, min)
# 剪接 -------------------------------------
                if cut != 1 :
                    file = final_clip
                else :
                    file = source_file
                    cut+=1

                clip1 = VideoFileClip(file).subclip(0, cutpoint)
                clip2 = VideoFileClip(file).subclip(after_ins_start, )
                final_clip = concatenate_videoclips([clip1, clip2])
            else:
                print(s,'pass')
                pass

        except sr.UnknownValueError:   
            Text = "無法翻譯"
        except sr.RequestError as e:
            Text = "無法翻譯{0}".format(e)

final_clip.write_videofile(outfile)