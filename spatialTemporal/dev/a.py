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
#expName=""
#dbConf=elib.data5
#[pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname]=[1,1,'test']
fptr=open(fname,"w")

win = visual.Window(units="pix", size=(500, 500), color=[0, 0, 0], fullscr=True)
mouse = event.Mouse(visible=False, newPos=[0,0], win=win) #mouse centered at zero
trialClock=core.Clock()
seed = random.randrange(1e6)
random.seed(seed)

blank=visual.TextStim(win,"")
obj=visual.GratingStim(win,tex='sin',ori=45,sf=1/50,mask='circle',size=256,contrast=.1)
noise = visual.NoiseStim(win,noiseType="white",blendmode="add",noiseElementSize=1,size=256,mask="circle")
noise2 = visual.NoiseStim(win,noiseType="white",noiseElementSize=1,size=256,mask="circle")
combo=visual.BufferImageStim(win,stim=(obj,noise))


win.flip()

a=event.waitKeys()





frames=[blank,combo,blank,obj,blank]
frameTimes=[100,100,165,100,10]
elib.runFrames(win,frames,frameTimes,trialClock)


a=event.waitKeys()


frames=[blank,obj,blank,noise2,blank]
frameTimes=[100,1,2,1,10]
elib.runFrames(win,frames,frameTimes,trialClock)

a=event.waitKeys()



frames=[blank,combo,blank]
frameTimes=[100,1,10]
elib.runFrames(win,frames,frameTimes,trialClock)


a=event.waitKeys()

fptr.flush()
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
win.close()
#elib.stopExp(sid,hz,resX,resY,seed,dbConf)
core.quit()
