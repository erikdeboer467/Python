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
from service.karoke_video_builder import KaraokeVideoBuilder
from service.moviepy_factory import create_progress_bar, createLyricTextClip
# endregion

config_default = {
    "work_directory": "D:\\Data\Documents\\_DEVELOPMENT\\Python\\blender\\!karaoke",
    "size": (1280, 720), # make sure background image is this size, don't forget the check the title color
    "how_many_pages": -1
    # "how_many_pages": 1
}

kvb = KaraokeVideoBuilder()

# title = "Kinderliedjes - De wielen van de bus"; title_color = "white"; font_size = 64
# title = "Kinderliedjes - Ik zag twee beren"; title_color = "black"; font_size = 64
# title = "Kinderliedjes - Dikkertje Dap"; title_color = "black"; font_size = 64 # .jpg removed by mistake.
title = "Kinderliedjes - Hoofd, schouders, knie en teen"; title_color = "black"; font_size = 50
config = { **config_default, "title": title, "font_size": font_size, "kbs_file": title + ".kbp", "background_pic": title + ".jpg", "title_color": title_color } # use - Karaoke Builder Studio - for lyric syncing 
# kvb.build({**config, "render": { "type": "preview", "audio": None                                                                             } })
# kvb.build({**config, "render": { "type": "render",  "audio": None,                          "output": title + " - karaoke - test.mp4"         } })
kvb.build({**config, "render": { "type": "render",  "audio": title + " - instrumental.mp3", "output": title + " - karaoke - instrumental.mp4" } })
kvb.build({**config, "render": { "type": "render",  "audio": title + " - vocals.mp3",       "output": title + " - karaoke - vocals.mp4"       } })
kvb.build({**config, "render": { "type": "render",  "audio": title + ".mp3",                "output": title + " - karaoke.mp4"                } })



# TODO:
# render time is long. 8 minutes per song +/-. there is no way to optimize that. moviepy is slow.
# * add support for duet
# parse json file slike "9307.json" and config it to kbp format
# endregion
