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


def runTrial(soa, stimCode):
    stim=[]
    stim.append(visual.TextStim(win, '+', pos = (-48,0.0)))
    stim.append(visual.TextStim(win, '+', pos = (48,0.0)))
    both=visual.BufferImageStim(win,stim=stim)
    stim.append(both)
    blank = visual.TextStim(win, '', pos = (0.0,0.0))
    if stimCode==2:
        frames = [blank, both, blank]
        frameTimes = [100,1,1]
    else:
        frames=[blank,stim[stimCode],blank,stim[1-stimCode],blank]
        frameTimes= [100,1,soa,1,1]
    elib.runFrames (win, frames, frameTimes, trialClock)
    keys = event.waitKeys(timeStamped=trialClock, 
                          keyList=['x', 'm', '9'])
    resp=1
    if keys[0][0]=='x':
        resp=0
    print(f"soa: {soa}, stim code: {stimCode}, resp: {resp}, ")
    return(resp)



def runBlock(n):
    for i in range(n):
        stim = random.choices(range(3),weights=[.25,.25,.5])[0]
        soa=random.choices([2,4,6],weights=[.33,.33,.33])[0]
        resp=runTrial(soa,stim)
        info=[i, stim, soa, resp]
        print(*info, sep=' ', file=fptr)


runBlock(60)








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