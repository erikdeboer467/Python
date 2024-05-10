# region Imports
import os
import re
from dataclasses import dataclass, field
import time
from moviepy.Clip import Clip
# from moviepy.editor import ImageClip, VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips, vfx, afx, CompositeAudioClip, ColorClip
from moviepy.editor import ImageClip, VideoFileClip, TextClip, AudioFileClip, CompositeVideoClip, ColorClip
# import numpy as np
# from PIL import Image, ImageDraw
from service.moviepy_factory import create_progress_bar, createLyricTextClip
# endregion

#region datamodel
@dataclass
class Word:
    start_ticks: int
    end_ticks: int
    word: str

@dataclass
class Line:
    words: list[Word] = field(default_factory=list)

@dataclass
class Page:
    lines: list[Line] = field(default_factory=list)
#endregion

class KaraokeVideoBuilder:
    def build(self, config: any):                
        #region parse kbs
        # ticks to seconds = ticks / 100D (150 = 1 second and 50 miliseconds, 1099 = 10 second and 99 miliseconds )
        def parseLyrics(kbs_file: str, lyric_to_upper = False):
            with open(os.path.join(config["work_directory"], config["kbs_file"]), 'r') as f:
                lines = f.read().splitlines()

            pages = list[Page]()

            for i in range(0, len(lines)):
                if 'PAGEV2' in lines[i]:
                    p = Page()
                    pages.append(p)

                    while True:
                        done = False
                        while not re.match(r"^[CLR]/[A-Za-z]/", lines[i]):
                            if len(lines[i]) > 0 and lines[i][0] == '-': done = True; break
                            i += 1
                        if done: break

                        lineItems = lines[i].split('/')
                        line = Line()
                        p.lines.append(line)
                        i += 1

                        while len(lines[i]) > 0 and lines[i][0] != '-' and not re.match(r"^[CLR]/[A-Za-z]/", lines[i]):
                            lineItems = lines[i].split('/')

                            line.words.append(Word(
                                start_ticks=int(lineItems[1]),
                                end_ticks=int(lineItems[2]),
                                word=lineItems[0].upper() if lyric_to_upper else lineItems[0]
                            ))

                            i += 1
            return pages

        def reportLyrics(lyrics: list[Page]):
            for p in lyrics:
                print('page:')
                for l in p.lines:
                    lineText = ''
                    fullLineText = ''
                    for w in l.words:
                        sSec = w.start_ticks / 100.0; eSec = w.end_ticks / 100.0
                        lineText += f'"{w.word}" [{w.start_ticks}-{w.end_ticks}] [{sSec}-{eSec}]; '
                        fullLineText += w.word
                    print(' > ' + lineText + " full='"+fullLineText+"'")
        # endregion

        lyrics = parseLyrics(os.path.join(config["work_directory"], config["kbs_file"]), True)
        # reportLyrics(lyrics)

        duration = lyrics[
            (config["how_many_pages"] if config["how_many_pages"] != -1 else 0)-1
        ].lines[-1].words[-1].end_ticks / 100.0 if not config["render"]["audio"] else \
            AudioFileClip(os.path.join(config["work_directory"], config["render"]["audio"])).duration

        clips: list[Clip] = [
            ColorClip(size=config["size"], color=(0x38/3,0x46/3,0xe1/3), duration=duration),
            # VideoFileClip(background_vid, target_resolution=size),
            ImageClip(os.path.join(config["work_directory"], config["background_pic"]), duration=duration)
        ]

        titleClip = TextClip(config["title"], font="Courier Bold", color=config["title_color"], fontsize=25, align="center")
        titleClip = titleClip.set_start(0)
        titleClip = titleClip.set_duration(duration)
        titleClip = titleClip.set_pos(('center','bottom'))
        clips.append(titleClip)


        previous_line_end_sec = 0
        for p in lyrics:    
            v_center_lines = len(p.lines) #5
            v_center_line_height = 69   
            v_center_paragraph_height = v_center_lines * v_center_line_height
            v_center_height = config["size"][1]        
            get_y = lambda v_center_line: (v_center_height - v_center_paragraph_height) / 2 + (v_center_line * v_center_line_height)

            page_start_previous_line_end_sec = previous_line_end_sec
            page_start_sec = p.lines[0].words[0].start_ticks / 100.0
            page_end_sec = p.lines[-1].words[-1].end_ticks / 100.0

            for index, l in enumerate(p.lines):
                lineText = ''

                line_start_sec = l.words[0].start_ticks / 100.0
                line_end_sec = l.words[-1].end_ticks / 100.0
                
                duration_since_last = line_start_sec - previous_line_end_sec
                if duration_since_last > 2:
                    progress = create_progress_bar(previous_line_end_sec, line_start_sec)
                    progress = progress.set_pos(('center', get_y(-1)))
                    clips.append(progress)

                word_timing: list[tuple] = []
                for w in l.words:
                    sSec = w.start_ticks / 100.0; eSec = w.end_ticks / 100.0
                    lineText += w.word
                    word_timing.append(((sSec, eSec), w.word))

                font_size = 64
                if "font_size" in config: font_size = config["font_size"]

                txtClip = createLyricTextClip(lineText, page_start_previous_line_end_sec, page_start_sec, page_end_sec, word_timing, font_size)
                txtClip = txtClip.set_pos(('center', get_y(index)))
                
                clips.append(txtClip)

                previous_line_end_sec = line_end_sec

            if config["how_many_pages"] != -1:
                config["how_many_pages"] -= 1
                if config["how_many_pages"] == 0: break

        final: CompositeVideoClip = CompositeVideoClip(clips)
        # final = final.set_audio(AudioFileClip(music_full)) 
        # final.write_videofile("combine.mp4", fps=24, codec='libx264')

        if config["render"]["type"] =="preview":
            print('Preview')
            final.preview(fps=24, audio=False)
        elif config["render"]["type"] == "render":
            print('Render: ' + config["render"]["output"])
            final.write_videofile(os.path.join(config["work_directory"], config["render"]["output"]), fps=24, codec='libx264', audio=os.path.join(config["work_directory"], config["render"]["audio"]), logger=None) # 18 sec, voor 1 page 
            # final.write_videofile("combine_instrumental.mp4", fps=24, codec='libx264', audio=music_instrumental, logger=None
            # final.write_videofile("combine_vocals.mp4", fps=24, codec='libx264', audio=music_vocals, logger=None)
            # final.write_videofile("combine.mp4", fps=24, codec='libx264', audio=music_full, logger=None)
            # alle 3 met audio = 695.40625 seconds = 11 1/2 minuut

