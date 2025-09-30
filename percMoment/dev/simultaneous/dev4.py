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
    stim.append(both)
    blank = visual.TextStim(win, '', pos = (0.0,0.0))

    frames = [blank, stim[stimCode], blank,stim[(1-stimCode)], blank]
    frameTimes = [100,1,dur,1,1]
    elib.runFrames (win, frames, frameTimes, trialClock)
    keys = event.waitKeys(timeStamped=trialClock, 
                          keyList=['x', 'm', '9'])
    resp=1
    if keys[0][0]=='x':
        resp=0
    return(resp)
    # resp "1/m" means same and "0/x" is diff ?



def runSim(trialNum):
    for i in range(trialNum):
        trialNum = i
        stim = random.choice([0,1,2])
        dur = random.choice([2,4,6])
        resp=runTrial(dur,stim)
        # staircase?
        info=[trialNum, dur, stim, resp]
        if info[2]==2:
            info[2] = 1
        else:
            info[2] = 0
        print(*info, sep=' ', file=fptr)


runSim(15)








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