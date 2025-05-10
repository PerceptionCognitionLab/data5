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
seed = random.randrange(1e6)
random.seed(seed)

grid = []
for i in range(5):
    for j in range(5):
        x = -96 + j*48
        y = -96 + i*48
        grid.append([x,y])
print(grid)

dots = []
for dot in grid:
    dots.append(visual.Circle(win, pos=(dot[0],dot[1]),fillColor=[1, 1, 1], radius=5))

mask=visual.BufferImageStim(win,stim=dots)
mask.draw()
win.flip()

a=event.waitKeys()


fptr.close()
win.close()
core.quit()