FONT_URL='media/wt003.ttf'
from moviepy import editor
import os.path as op

def annotate(clip, txt, txt_color='red', fontsize=50, font='Xolonium-Bold'):
    """ Writes a text at the bottom of the clip. """
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=FONT_URL, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)

video = editor.VideoFileClip("media/IMG_9589.MOV")
subs = [((0, 15), '他穿起來舒適跟痛風性是很舒服的一個版型這兩款單品或是搭配在一起還是分開來當都算得還蠻好大的一套'), 
        ((19, 21), '剪接'), 
        ((40, 50), '舒服的一個版型這兩款單品或是搭配在一起還是分開來的都算還蠻好搭皮套再來這間了它是一間')]
annotated_clips = [annotate(video.subclip(from_t, to_t), txt) for (from_t, to_t), txt in subs]
final_clip = editor.concatenate_videoclips(annotated_clips)
final_clip.write_videofile("media/IMG_9589_sub.mp4")