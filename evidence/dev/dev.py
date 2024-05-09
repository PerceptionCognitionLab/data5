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
mu = 10
sd = 25
numDots = 30
dotY = 0
dotRadius = 5
clock = core.Clock()

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
correctSound1 = sound.Sound(500,secs = 0.25)
correctSound2 = sound.Sound(1000,secs = 0.25)
incorrectSound1 = sound.Sound(500,secs = 0.5)
incorrectSound2 = sound.Sound(375,secs = 0.5)
xAxis = visual.Line(win,start=(0,-500),end=(0,500),lineColor=[255,0,0],lineWidth=0.5)
yAxis = visual.Line(win,start=(-1000,0),end=(1000,0),lineColor=[255,0,0],lineWidth=0.5)

def playCorrectSound():
    correctSound1.play()
    core.wait(0.25)
    correctSound2.play()
    core.wait(0.25)

def playIncorrectSound():
    incorrectSound1.play()
    incorrectSound2.play()
    core.wait(0.5)

def countdown():
    win.flip()
    core.wait(0.5)
    marker = visual.Circle(win,pos=(0,0),fillColor=[255,0,0],radius=5)
    marker.draw()
    xAxis.draw()
    yAxis.draw()
    win.flip()
    core.wait(0.5)
    marker = visual.Circle(win,pos=(0,0),fillColor=[255,255,0],radius=5)
    marker.draw()
    xAxis.draw()
    yAxis.draw()
    win.flip()
    core.wait(0.5)
    marker = visual.Circle(win,pos=(0,0),fillColor=[0,255,0],radius=5)
    marker.draw()
    xAxis.draw()
    yAxis.draw()
    win.flip()
    core.wait(0.5)

def displayDots(mu,sd,numDots,dotY,dotRadius):
    neg = rng.integers(0,2)
    if(neg == 0):
        correct = -1
    else:
        correct = 1
    coordinates = []
    for i in range(numDots+1):
        coordinates.append(np.round(np.random.normal(mu*(neg*2-1),sd)))
    responseTime = clock.getTime()
    xAxis.draw()
    yAxis.draw()
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
                playCorrectSound()
            else:
                playIncorrectSound()
            responseTime = clock.getTime()-responseTime
            return [*coordinates,correct,-1,i,responseTime]
        if(event.getKeys(['m'])):
            if(correct == 1):
                playCorrectSound()
            else:
                playIncorrectSound()
            responseTime = clock.getTime()-responseTime
            return [*coordinates,correct,1,i,responseTime]
    playIncorrectSound()
    responseTime = clock.getTime()-responseTime
    return [*coordinates,correct,0,i,responseTime]

numTrials = 5
for i in range(numTrials):
    countdown()
    output=[pid,sid,i+1]+displayDots(mu,sd,numDots,dotY,dotRadius)
    print(*output,sep=", ", file=fptr)
# playCorrectSound()

fptr.flush()
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
win.close()


#elib.stopExp(sid,hz,resX,resY,seed,dbConf)
core.quit()