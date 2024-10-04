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
continueKey = ['Enter']
refreshRate=165
elib.setRefreshRate(refreshRate)
expName="ev1"
dbConf=elib.data5
#[pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname]=[1,1,'test']
fptr=open(fname,"w")
mu = 10
sd = 25
numDots = 30
dotY = 0
dotRadius = 5
dotInterval = 0.3
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

def ready():
    visual.TextStim(win, text="Ready? Press any key to continue.", height=30, color='white').draw()
    win.flip()
    while(True):
        if(event.getKeys(abortKey)):
            win.close()
            core.quit()
        if(event.getKeys()):
            break

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
    core.wait(0.5 + np.random.normal(0,0.1))

def manualTutorial():
    ready()
    coordinates = [10,87,44,-49,-10,-71,-31,18,13,-37,42,-97,-70,-88]
    for i in range(len(coordinates)):
        if(i == 0 or i == 3 or i == 6):
            countdown()
        circ=visual.Circle(win, pos=(coordinates[i],dotY), fillColor=[1, 1, 1], radius=dotRadius)
        frame = visual.BufferImageStim(win,stim=[xAxis,yAxis,circ])
        frame.draw()
        win.flip()
        event.clearEvents()
        while(True):
            if(event.getKeys(abortKey)):
                win.close()
                core.quit()
            if(i == 2):
                if(event.getKeys('m')):
                    playCorrectSound()
                    break
            elif(i == 5 or i == 13):
                if(event.getKeys('x')):
                    playCorrectSound()
                    break
            else:
                if(event.getKeys('space')):
                    break

def autoTutorial(trial,interval):
    coordinates = []
    for i in range(numDots):
        coordinates.append(np.round(np.random.normal(mu*trial,sd)))
    for i in range(len(coordinates)):
        event.clearEvents()
        circ=visual.Circle(win, pos=(coordinates[i],dotY), fillColor=[1, 1, 1], radius=dotRadius)
        frame = visual.BufferImageStim(win,stim=[xAxis,yAxis,circ])
        currentFrame = 0
        for currentFrame in range(round(refreshRate*interval)):
            responseTime = round(clock.getTime(),3)
            if(event.getKeys(abortKey)):
                win.close()
                core.quit()
            if(event.getKeys(['x'])):
                if(trial == -1):
                    playCorrectSound()
                else:
                    playIncorrectSound()
                return
            if(event.getKeys(['m'])):
                if(trial == 1):
                    playCorrectSound()
                else:
                    playIncorrectSound()
                return
            frame.draw()
            win.flip()
    playIncorrectSound()
        
def displayDots(mu,sd,numDots,dotY,dotRadius,feedback):
    neg = rng.integers(0,2)
    if(neg == 0):
        correct = -1
    else:
        correct = 1
    coordinates = []
    for i in range(numDots):
        coordinates.append(np.round(np.random.normal(mu*(neg*2-1),sd)))
    clock.reset()
    for i in range(len(coordinates)):
        event.clearEvents()
        circ=visual.Circle(win, pos=(coordinates[i],dotY), fillColor=[1, 1, 1], radius=dotRadius)
        frame = visual.BufferImageStim(win,stim=[xAxis,yAxis,circ])
        currentFrame = 0
        for currentFrame in range(round(refreshRate*dotInterval)):
            responseTime = round(clock.getTime(),3)
            if(event.getKeys(abortKey)):
                win.close()
                core.quit()
            if(event.getKeys(['x'])):
                if(feedback == 0):    
                    if(correct == -1):
                        playCorrectSound()
                    else:
                        playIncorrectSound()
                return [*coordinates,correct,-1,i,responseTime]
            if(event.getKeys(['m'])):
                if(feedback == 0):
                    if(correct == 1):
                        playCorrectSound()
                    else:
                        playIncorrectSound()
                return [*coordinates,correct,1,i,responseTime]
            frame.draw()
            win.flip()
    playIncorrectSound()
    return [*coordinates,correct,0,i,responseTime]

manualTutorial()
tutorialAnswers = [1,-1,-1,1]
for i in range(4):
    if(i == 0 or i == 2):
        ready()
    if(i < 2):
        interval = 1
    else:
        interval = 0.3
    countdown()
    autoTutorial(tutorialAnswers[i],interval)
    
numBlocks = 3
numTrials = 3
for j in range(numBlocks):
    ready()
    for i in range(numTrials):
        countdown()
        output=[pid,sid,j+1,i+1]+displayDots(mu,sd,numDots,dotY,dotRadius,j)
        print(*output,sep=", ", file=fptr)

fptr.flush()
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
win.close()


#elib.stopExp(sid,hz,resX,resY,seed,dbConf)
core.quit()