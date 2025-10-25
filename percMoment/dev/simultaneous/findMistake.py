# Imports
from psychopy import core, visual, sound, event, clock
import math 
import random
import decimal
import sys
import numpy as np  
import os
import time   
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as elib

# Housekeeping
abortKey=['9']
refreshRate=165
elib.setRefreshRate(refreshRate)
expName="test"
dbConf=elib.data5
#[pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname]=[1,1,'test']
fptr=open(fname,"w")

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
mouse = event.Mouse(visible=False, newPos=[0,0], win=win) 
trialClock=core.Clock()
correctSound1=sound.Sound(value=500,secs=.1)
correctSound2=sound.Sound(value=1000,secs=.2)
errorSound=sound.Sound(value=300,secs=.5)
seed = random.randrange(1e6)
random.seed(seed)

blank = visual.TextStim(win, '', pos = (0.0,0.0))
option = []
#option.append(visual.TextBox(win, text = "Simultaneous", font_size=18, font_color=[-1,-1,1], color_space='rgb', size=(1.8,.1), pos=(-96,0.0)))
#option.append(visual.TextBox(win, text = "Non-Simultaneous", font_size=18, font_color=[-1,-1,1], color_space='rgb', size=(1.8,.1), pos=(96,0.0)))
#options=visual.BufferImageStim(win,stim=option)
#easy=visual.TextStim(win,"help")
easy=visual.TextBox2(win, text = "Non-Simultaneous")

#frames = [blank, stim[stimCode], blank,stim[(1-stimCode)], blank]
frames = [blank,easy]
frameTimes = [100,1]
stamps=elib.runFrames(win, frames, frameTimes, trialClock,addBlank=False)
event.waitKeys()

fptr.close()
win.close()
core.quit()

