import math
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, vfx, afx, CompositeAudioClip, ColorClip
from moviepy.video.fx.all import crop
import numpy
from PIL import Image, ImageDraw
import numpy
from PIL import Image, ImageDraw



def createLyricTextClip(line_text: str, inactive_start: int, start: int, end: int, base_timing: any, font_size: any = 64, stroke_width = 6, color="white", stroke_color='black'):
    def progress_effect(clip, parent_start: int, timing, color_left_done = (0, 160, 239), color_right_todo = (255, 255, 255)):
        def effect(get_frame: callable, t: numpy.float64):
            tb = t
            t += parent_start #t is the time in the textstrip and start for every timestrip at 0

            img: Image.Image = Image.fromarray(get_frame(t))
            width, height = img.size

            if t >= inactive_start and t < start:
                arr = numpy.array(img) 

                # arr[0 : height, 0 : width] = (0x38/3,0x46/3,0xe1/3)  

                # # color=(0x38/3,0x46/3,0xe1/3)
                step_count = inactive_start - start
                r_step = (15-255) / step_count
                g_step = (23-255) / step_count
                b_step = (75-255) / step_count

                arr[0 : height, 0 : width] = (15+tb*r_step,23+tb*g_step,75+tb*b_step)

                # dit kan beter.

            else:
                x = 0

                for e in timing:
                    secStartStop, segmentPXWidth, text = e
                    secStart, secStop = secStartStop
                
                    # print(t, text)

                    if t >= secStart and t <= secStop: #isActive
                        duration = secStop - secStart 
                        widthDurationRatio = segmentPXWidth / duration
                        correctTime = t - secStart
                        x += int(correctTime * widthDurationRatio)                
                    elif t > secStop: #isDone:
                        x += segmentPXWidth
                    # elif t < secStart: #isTodo
                    #     pass

                arr = numpy.array(img) 

                arr[0 : height, 0 : x] = color_left_done
                arr[0 : height, x : width] = color_right_todo

            return numpy.array(Image.fromarray(arr))
        return clip.fl(effect)

    # region Add custom font
    # C:\Program Files\ImageMagick-7.1.1-Q16-HDRI
    # type-ghostscript.xml 
    # <type name="HelveticaNeueLTPro" fullname="HelveticaNeueLTPro" family="HelveticaNeueLTPro" style="normal" weight="400" stretch="normal" format="type1" metrics="C:\Users\erikd\AppData\Local\Microsoft\Windows\Fonts\HelveticaNeueLTPro-BlkCn.otf" glyphs="C:\Users\erikd\AppData\Local\Microsoft\Windows\Fonts\HelveticaNeueLTPro-BlkCn.otf" />
    # endregion

    font = "HelveticaNeueLTPro"
    # font = "Helvetica-Bold"
    
    txtClip = TextClip(line_text, font=font, color=color, 
                        fontsize=font_size, align="center", stroke_width=stroke_width, 
                        stroke_color=stroke_color)
    txtClip = txtClip.set_start(inactive_start)
    txtClip = txtClip.set_duration(end-inactive_start)
    txtClip = txtClip.set_pos(('center','center'))
    txtClip = txtClip.fx(vfx.fadein, start-inactive_start)

    timing = [(
        e[0], TextClip(e[1], font=font, color=color, fontsize=font_size, align="center").size[0], e[1]        
    ) for e in base_timing] # (seconds from, seconds to), width text in pixcels, text

    pTxtClip = TextClip(line_text, font=font, color=color, fontsize=font_size, align="center")
    pTxtClip = pTxtClip.set_start(inactive_start)
    pTxtClip = pTxtClip.set_duration(end-inactive_start)
    pTxtClip = pTxtClip.set_pos(('center','center'))
    pTxtClip = progress_effect(pTxtClip, inactive_start, timing)
    pTxtClip = pTxtClip.fx(vfx.fadein, start-inactive_start)
        
    return CompositeVideoClip([txtClip, pTxtClip])

def create_progress_bar(start: int, end: int):
    def rec_progress_effect(clip, parent_start: int, duration: int, color_left_done = (0, 160, 239), color_right_todo = (255, 255, 255)):
        def effect(get_frame: callable, t: numpy.float64):
            # t += parent_start #t is the time in the textstrip and start for every timestrip at 0

            f = get_frame(t).astype("uint8")
            img: Image.Image = Image.fromarray(f)

            width, height = img.size
            widthDurationRatio = width / duration
            x = int(t * widthDurationRatio)                

            arr = numpy.array(img) 

            arr[0 : height, 0 : x] = color_left_done
            arr[0 : height, x : width] = color_right_todo

            return numpy.array(Image.fromarray(arr))
        return clip.fl(effect)

    duration = end - start

    rec: ColorClip = ColorClip(size=(300, 10), color=(255, 255, 255))
    rec = rec.set_start(start)
    rec = rec.set_duration(duration)
    rec = rec_progress_effect(rec, start, duration)
    rec = rec.margin(2)
    return rec
    