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



def runTrial(dur, stimCode):
    stim=[]
    stim.append(visual.TextStim(win, '+', pos = (-48,0.0)))
    stim.append(visual.TextStim(win, '+', pos = (48,0.0)))
    both=visual.BufferImageStim(win,stim=stim)
    blank = visual.TextStim(win, '', pos = (0.0,0.0))

    frames = [blank, stim[stimCode], both, blank]
    frameTimes = [100,dur,100,1]
    elib.runFrames (win, frames, frameTimes, trialClock)
    keys = event.waitKeys(maxWait=5, timeStamped=trialClock, 
                          keyList=['x', 'm', '9'])
    resp=1
    if keys[0]=='x':
        resp=0
    return(resp)



def runSim(trialNum):
    for i in range(trialNum):
        trialNum = i
        stim = random.choice([0,1])
        dur = random.choice([1, 2, 5, 10, 20])
        resp=runTrial(dur,stim)
        info=[trialNum, stim, dur, resp]
        print(*info, sep=' ', file=fptr)


runSim(3)








# frames = [blank, both, blank]
# frameTimes = [100,100,1]
# elib.runFrames (win, frames, frameTimes, trialClock)

# frames = [blank, stim2,both, blank]
# frameTimes = [100,2,100,1]
# elib.runFrames (win, frames, frameTimes, trialClock)

# a=event.waitKeys()


fptr.close()
win.close()
core.quit()