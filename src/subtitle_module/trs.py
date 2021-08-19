FONT_URL='/home/ball45/Downloads/TaipeiSansTCBeta-Light.ttf'
from moviepy import editor
import os.path as op

# handling with video source
source_file = input('Enter your video stream and file name:')
slash_pos = source_file.rfind('/')
dot_pos = source_file.rfind('.')
source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
source_clip = editor.VideoFileClip(source_file)

# handling with subtitle file
subtitle_file = open(source_path + source_name + '.srt')
subtitle_line = subtitle_file.readlines()
subtitle_file.close()

class Subtitle:
    def __init__(self, time_start, time_end, string=' '):
        self.time_start = time_start
        self.time_end = time_end
        self.string = string

    def get_prev_timeslice(self): # get time_start - 1 ms
        start_time_ms = int(self.time_start[9:])
        if start_time_ms != 0:
            return self.time_start[:9] + str(start_time_ms - 1).zfill(3)
        else:
            return self.time_start[:6] + \
             str(int(self.time_start[6:8]) - 1).zfill(2) + ",999"

    def get_next_timeslice(self): # get time_end + 1 ms
        end_time_ms = int(self.time_end[9:])
        if end_time_ms != 999:
            return self.time_end[:9] + str(end_time_ms + 1).zfill(3)
        else:
            return self.time_end[:6] + \
             str(int(self.time_end[6:8]) + 1).zfill(2) + ",000"



subtitle_list = []
for index in range(0, len(subtitle_line), 4):
    string = subtitle_line[index + 2]
    time_start = subtitle_line[index + 1][:12]
    time_end = subtitle_line[index+1][17:29]
    subtitle_list.append(Subtitle(time_start, time_end, string))

# add clip without subtitle into subtitle_list
i = 0
while i < len(subtitle_list) - 1:
    if subtitle_list[i].time_end < subtitle_list[i+1].time_start:
        time_start = subtitle_list[i].time_end
        time_end = subtitle_list[i+1].time_start
        # time_start = subtitle_list[i].get_next_timeslice()
        # time_end = subtitle_list[i+1].get_prev_timeslice()
        subtitle_list.insert(i+1, Subtitle(time_start, time_end))
        i += 1

    i += 1


def export_srt_file(subtitle_list, filename=source_name+'_new_2', filepath=source_path):
    f = open(filepath+filename+'.srt', 'w')
    for i in range(len(subtitle_list)):
        f.write(str(i) + '\n')
        f.write(subtitle_list[i].time_start + ' --> ' + subtitle_list[i].time_end + '\n')
        f.write(subtitle_list[i].string + '\n')

    f.close()

export_srt_file(subtitle_list)

def annotate(clip, txt, txt_color='red', fontsize=50, font='Xolonium-Bold'):
    """ Writes a text at the bottom of the clip. """
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=FONT_URL, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)

# bind subtitle file into video stream
annotated_clips = []
for subtitle in subtitle_list:
    annotated_clips.append(annotate(source_clip.subclip(subtitle.time_start, subtitle.time_end), subtitle.string))

final_clip = editor.concatenate_videoclips(annotated_clips)
final_clip.write_videofile("movie_output.mp4")