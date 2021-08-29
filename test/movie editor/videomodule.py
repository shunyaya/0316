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
source_file = "media/tetest.mp4"
slash_pos = source_file.rfind('/')
dot_pos = source_file.rfind('.')
source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
wavfile = source_path + source_name + '.wav'
outfile = source_path + source_name + '_out.mp4'

if not os.path.exists(wavfile):
    os.system("ffmpeg -i "+source_file+" "+source_path + source_name + '.wav')

clip = VideoFileClip(source_file)
new_frame = []

#轉灰階--------------------------------------
for frames in clip.iter_frames():
    gray = cv.cvtColor(frames, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray) #播放灰階影片
    new_frame.append(gray)
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# 找出fps---------------------------------------
def cap_fps(major_ver):
    
    if int(major_ver)  < 3 :
        fps = clip.get(cv.CV_CAP_PROP_FPS)
    else :
        fps = clip.get(cv.CAP_PROP_FPS)
    
    return fps

clip = cv.VideoCapture(source_file)
# Find OpenCV version
(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')
fps = int(cap_fps(major_ver)) 
clip.release()

# 測試靜音 ----------------------------------
record_start = np.zeros(1000)
record_end = np.zeros(1000)
duration = np.zeros(1000)
speech = np.zeros(1000)
num = 0
section=[]
cut=1

# split returns a generator of AudioRegion objects
sound = AudioSegment.from_file(wavfile, format="wav") 
audio_regions = auditok.split(
    wavfile,
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
    # evaluate silence section length
    duration[j] = record_start[j+1] - record_end[j]
    print("Silence ", j, " :", round(record_end[j], 3), 's', 'to', round(record_start[j+1], 3), 's, Duration : ', duration[j])

    # if there are two continuous silence sections >2.5 
    if duration[j-1] > 1.4 and duration[j] > 1.4 and speech[j] < 5.0:
        print("instruction : ", round(record_start[j], 3), 's', 'to', round(record_end[j], 3), 's')
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
                front = int(record_end[j-1])
                if (front-5) < 0 :
                    ex=0
                else :
                    ex=front-5
            # 偵測重複 ----------------------------------

                min = 1000000
                sum = 0
                summ = 0
                # 比較第t秒和第cutpoint秒的frames，一秒鐘有30個frame(fps=30)
                for cutpoint in range(int(record_start[j+1]),int(record_start[j+1])+2) :
                    for t in range(ex,front):
                        for k in range(fps*2):
                            for i in np.square(new_frame[t*fps+k] - new_frame[cutpoint*fps+k]):
                                sum = sum + i
                        for j in sum :
                            summ = summ + j   
                        #print('t : ', t, ' - ',cutpoint,' =', summ, '\n')
                        if min>summ :
                            t1 = t
                            t2 = cutpoint
                            min = summ   
                        sum = 0
                        summ = 0
                #輸出t1和t2最相近
                print (t1,t2,min)
            # 剪接 -------------------------------------
                if cut != 1 :
                    file = final_clip
                else :
                    file = source_file

                clip1 = VideoFileClip(file).subclip(0, t1)
                clip2 = VideoFileClip(file).subclip(t2, )
                final_clip = concatenate_videoclips([clip1, clip2])
                cut+=1
            else:
                print(s,'pass')

        except sr.UnknownValueError:   
            Text = "無法翻譯"
        except sr.RequestError as e:
            Text = "無法翻譯{0}".format(e)

final_clip.write_videofile(outfile)