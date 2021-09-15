import speech_recognition as sr


def DetectIns(wavfile,ins_start):
    r = sr.Recognizer()
    instruction = sr.AudioFile(wavfile)
    with instruction as source:
        audio = r.record(source, offset = ins_start, duration = 5)
    try:
        ins = r.recognize_google(audio_data=audio, key=None,language="zh-TW", show_all=True)  # show_all=True
        if "剪接" in str(ins):
            print("Instruction: 剪接")
        else:
            print("Instruction: ", ins)
            pass

    except sr.UnknownValueError:
        ins = "無法翻譯"
    except sr.RequestError as e:
        ins = "無法翻譯{0}".format(e)

if __name__ == "__main__" :
    DetectIns(10.35)