from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random  
import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as elib
seed = 1
rng = random.default_rng(seed)

refreshRate=165
elib.setRefreshRate(refreshRate)
expName="devEv"
dbConf=elib.beta
#[pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname]=[1,1,'test']
fptr=open(fname,"w")

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
correctSound1 = sound.Sound(500,secs = 0.25)
correctSound2 = sound.Sound(1000,secs = 0.25)

def playSound():
    correctSound1.play()
    core.wait(0.25)
    correctSound2.play()
    core.wait(0.25)

def displayDots(mu,sd):
    neg = rng.integers(0,2)
    if(neg == 0):
        correct = -1
    else:
        correct = 1
    coordinates = []
    for i in range(31):
        coordinates.append(np.round(np.random.normal(mu*(neg*2-1),sd)))
    for i in range(len(coordinates)):
        circ=visual.Circle(win, pos=(coordinates[i],0), fillColor=[1, 1, 1], radius=5)
        circ.draw()
        win.flip()
        core.wait(.3)
        if(event.getKeys(['x'])):
            if(correct == -1):
                playSound()
            return [coordinates,correct,-1,i]
        if(event.getKeys(['m'])):
            if(correct == 1):
                playSound()
            return [coordinates,correct,1,i]
    return [coordinates,correct,0,i]

def block(numTrials,mu,sd):
    correctResponse = []
    numDots = []
    coordinates = []
    for i in range(numTrials):
        data = displayDots(mu,sd)
        correctResponse.append(data[0]==data[1])
        numDots.append(data[2])
        coordinates.append(data[3])
    return [correctResponse,numDots,coordinates]

numTrials = 5
for i in range(5):
    output=[pid,sid,i+1]+displayDots(25,125)
    print(*output,sep=", ", file=fptr)


fptr.flush()
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
win.close()


#elib.stopExp(sid,hz,resX,resY,seed,dbConf)
core.quit()