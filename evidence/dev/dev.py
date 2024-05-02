from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random  
import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as elib

#random
rng = random.default_rng()
seed = random.randint(1,1000000)
rng = random.default_rng(seed)

#globals
abortKey = ['9']
refreshRate=165
elib.setRefreshRate(refreshRate)
expName="devEv"
dbConf=elib.beta
#[pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname]=[1,1,'test']
fptr=open(fname,"w")
mu = 25
sd = 125
numDots = 30
dotY = 0
dotRadius = 5

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
correctSound1 = sound.Sound(500,secs = 0.25)
correctSound2 = sound.Sound(1000,secs = 0.25)

def playSound():
    correctSound1.play()
    core.wait(0.25)
    correctSound2.play()
    core.wait(0.25)

def displayDots(mu,sd,numDots,dotY,dotRadius):
    win.flip()
    core.wait(0.5)
    marker = visual.Circle(win,pos=(0,0),fillColor=[255,0,0],radius=5)
    marker.draw()
    win.flip()
    core.wait(0.5)
    marker = visual.Circle(win,pos=(0,0),fillColor=[255,255,0],radius=5)
    marker.draw()
    win.flip()
    core.wait(0.5)
    marker = visual.Circle(win,pos=(0,0),fillColor=[0,255,0],radius=5)
    marker.draw()
    win.flip()
    core.wait(0.5)
    neg = rng.integers(0,2)
    if(neg == 0):
        correct = -1
    else:
        correct = 1
    coordinates = []
    for i in range(numDots+1):
        coordinates.append(np.round(np.random.normal(mu*(neg*2-1),sd)))
    for i in range(len(coordinates)):
        circ=visual.Circle(win, pos=(coordinates[i],dotY), fillColor=[1, 1, 1], radius=dotRadius)
        circ.draw()
        win.flip()
        core.wait(.3)
        if(event.getKeys(abortKey)):
            win.close()
            core.quit()
        if(event.getKeys(['x'])):
            if(correct == -1):
                playSound()
            return [*coordinates,correct,-1,i]
        if(event.getKeys(['m'])):
            if(correct == 1):
                playSound()
            return [*coordinates,correct,1,i]
    return [*coordinates,correct,0,i]

numTrials = 5
for i in range(numTrials):
    output=[pid,sid,i+1]+displayDots(mu,sd,numDots,dotY,dotRadius)
    print(*output,sep=", ", file=fptr)


fptr.flush()
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
win.close()


#elib.stopExp(sid,hz,resX,resY,seed,dbConf)
core.quit()