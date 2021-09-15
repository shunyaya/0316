import os
mp4file = "media/testttt720.MOV"
mp3file = "media/tai.wav"
os.system("ffmpeg -i "+mp3file+" "+mp4file)