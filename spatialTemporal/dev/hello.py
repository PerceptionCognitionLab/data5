from psychopy import prefs  
prefs.hardware['audioLib']=['PTB']
prefs.hardware['audioLatencyMode']=3
from psychopy import core, visual, sound, event
import numpy as np
from numpy import random
import sys
import math
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as el


scale=400

trialClock=core.Clock()

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)


hello=visual.TextStim(win,"Hello World")
blank=visual.TextStim(win,"")

frames=[blank,hello,blank]
frameTimes=(165,165,1)
el.runFrames(win,frames,frameTimes,trialClock)


win.close()
core.quit()