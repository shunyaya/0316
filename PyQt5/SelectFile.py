import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import numpy as np
import auditok
from pydub import AudioSegment
import speech_recognition as sr
from moviepy.editor import *
import cv2 as cv

class ListViewDemo(QWidget):
    def __init__(self, parent = None):
        super(ListViewDemo, self).__init__(parent)
        self.setWindowTitle('智慧影音接軌')
        self.resize(500,270)
        self.initUI()
       
    def initUI(self):
        layout = QVBoxLayout()
        self.listWidget = QListWidget()

        self.buttonOpenFile = QPushButton('Select File')
        self.buttonOpenFile.clicked.connect(self.LoadPath) 
        layout.addWidget(self.buttonOpenFile)

        self.buttonRemoveFile = QPushButton('Remove File')
        self.buttonRemoveFile.clicked.connect(self.RemovePath)
        layout.addWidget(self.buttonRemoveFile)

        self.buttonRemoveAll = QPushButton('Remove All')
        self.buttonRemoveAll.clicked.connect(self.DelListItem)
        layout.addWidget(self.buttonRemoveAll)

        self.listview = QListView()
        #建立一個空的模型
        self.listModle = QStringListModel()
        #self.list = ["列表項1", "列表項2", "列表項3"]
         #將數據放到空的模型內
        #self.listModle.setStringList(self.list)
        self.listview.setModel(self.listModle)
        layout.addWidget(self.listview)

        self.combobox = QComboBox()
        self.combobox.setItemText(3, "Tw")
        layout.addWidget(self.combobox)

        self.buttonClip = QPushButton('Edit Video')
        self.buttonClip.clicked.connect(self.VideoEdit)
        layout.addWidget(self.buttonClip)

        self.setLayout(layout)
    

    def LoadPath(self):
        fname,_ = QFileDialog.getOpenFileName(self, '打開文件', '.', '文件(*.MOV *.mp4)')
        if len(fname) != 0 :
            row = self.listModle.rowCount()  # 獲得最後一行的行數       
            self.listModle.insertRow(row)  # 數據模型添加行
            index = self.listModle.index(row,0)  # 獲得數據模型的索引
            self.listModle.setData(index,fname) 
        print(self.listModle.stringList())
            
    def RemovePath(self):
        selected  = self.listview.selectedIndexes() # 根據所有獲取item
        for i in selected:
            self.listModle.removeRow(i.row())
    
    def DelListItem(self):
        row1 = self.listModle.rowCount()
        for i in range(row1):
            self.listModle.removeRow(self.listview.modelColumn())

    def VideoEdit(self):
        # mp4 轉成 wav -----------------------------
        #inputfile = "media/tainanvlog.mp4"
        row = self.listModle.rowCount()
        for i in range(row):
            source_file = self.listModle.stringList()[i]
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

            # 辨識是否為語音指令“剪接” ---------------------------
                    r = sr.Recognizer()
                    instruction = sr.AudioFile(wavfile)
                    with instruction as source:
                        audio = r.record(source, offset = record_start[j], duration = 5)
                    try:
                        ins = r.recognize_google(audio_data=audio, key=None,language="zh-TW", show_all=True)
                        if "剪接" in str(ins):
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
                            print(ins,'pass')
                            pass

                    except sr.UnknownValueError:   
                        ins = "無法翻譯"
                    except sr.RequestError as e:
                        ins = "無法翻譯{0}".format(e)

            final_clip.write_videofile(outfile)
            final_clip.close()


                
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('./PyQt5/1179069.png'))
    win = ListViewDemo()
    win.show()
    sys.exit(app.exec_())