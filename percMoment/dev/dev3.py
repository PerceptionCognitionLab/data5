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

refreshRate=165
elib.setRefreshRate(refreshRate)
expName="pmDev"
dbConf=elib.beta
#[pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
pid=1
sid=1
fname="test"
fptr=open(fname,"w")

# Define variables
scale = 250
win = visual.Window(units="pix", size=(2 * scale, 2 * scale), color=[-1, -1, -1], fullscr=True)
spacing = 48 # spacing between dots
correct1 = sound.Sound(500,secs = .1) # correct response
correct2 = sound.Sound(1000,secs = .2) 
mouse = event.Mouse(visible=False, newPos=[0,0], win=win) #mouse centered at zero
trialClock=core.Clock()

fix = visual.TextStim(win, "+")  # fixation cross
blank = visual.TextStim(win, "")  # blank window
numTrials = 10 # number of trials
z = 0 # counter for trial_Frames adjustment based on correctness
seed = random.randrange(1e6)
rng = random.Random(seed)
abortKey=['9']

# Define functions

def makeDotIndex(target):
    tot = np.array(range(49))
    wot = np.delete(tot, target)
    index = np.array(range(48))
    iA = np.sort(np.random.choice(index, 24, replace=False))
    iB = np.delete(index, iA)
    return [wot[iA], wot[iB]]

def mouseOnResp(x, y, mousePos, crit=20):
    dlc = []
    for i in range(len(x)):
        dist = np.linalg.norm([x[i], y[i]] - mousePos)
        dlc.append(dist < crit)
    S = sum(bool(x) for x in dlc)
    if S == 1:
        out = np.where(dlc)[0][0]
    else: 
        out = -1    
    return out

def adjustSOA(soa,correct,correctPrevious):
    if (correct and correctPrevious==1):
    	soa+=1
    	cv=0
    if (correct and correctPrevious==0):
    	cv=1   
    if (not correct):
        soa-=1
        cv=0
    if (soa==0):
     	soa=1
    return ([soa,cv]) 

#Audio feedback
def correctSound(correct):
	if correct:
		correct1.play()
		correct2.play()

# Make_ trials experiment portion of code
x = []
y = []

for i in range(49):
    result = divmod(i, 7)
    x.append(spacing * (result[0] - 3))
    y.append(spacing * (result[1] - 3))
    

perimeter = [0,1,2,3,4,5,6,7,13,14,20,21,27,28,34,35,41,42,43,44,45,46,47,48] # excluded target points on perimeter of 7 x 7 square
valid_points = [i for i in range(49) if i not in perimeter]


#########################################################################################################################


def doTrial(soa):
    target = random.choice(valid_points)
    [aDots, bDots] = makeDotIndex(target)
    dots=[]
    for i in range(len(aDots)):
        dots.append(visual.Circle(win, pos=(x[aDots[i]],y[aDots[i]]), fillColor=[1, 1, 1], radius=5))
    a=visual.BufferImageStim(win,stim=dots)
    dots=[]
    for i in range(len(bDots)):
        dots.append(visual.Circle(win, pos=(x[bDots[i]],y[bDots[i]]), fillColor=[1, 1, 1], radius=5))
    b=visual.BufferImageStim(win,stim=dots)
    dots=[]
    for i in range(len(x)):
        dots.append(visual.Circle(win, pos=(x[i],y[i]), fillColor=[0, -1, -1], radius=2.5))
    all=visual.BufferImageStim(win,stim=dots)	
    frame = [fix, blank, a, blank, b, blank, all]
    frameDurations = [120, 60, 1, soa, 1, 60, 1]
    stamps=elib.runFrames(win,frame,frameDurations,trialClock)
# Get Choice		
    mousePress = False
    mouse.setVisible(True)
    mouse.setPos((300,0))
    while not mousePress:
        buttons = mouse.getPressed(getTime=False)
        resp = mouseOnResp(x, y, mouse.getPos())
        frame[6].draw()
        if resp > -1: 
            respDot = visual.Circle(win, pos=(x[resp], y[resp]), fillColor=[1, 1, 1], radius=2)
            respDot.draw()
        win.flip()
        mousePress = any(buttons)
# Give Feedback
    correct = resp == target
    correctSound(correct)
    print(pid,sid,soa,target,resp,correct,sep=", ", file=fptr)
    fptr.flush()
    mouse.setVisible(False)
    return(correct)


soa=1
correctPrevious=0
for n in range(numTrials):
	correct=doTrial(soa)
	[soa,correctPrevious]=adjustSOA(soa,correct,correctPrevious)


visual.TextStim(win,"Thank You").draw()
win.flip()
a=event.waitKeys(keyList=abortKey)
hz=round(win.getActualFrameRate())
size=win.size

win.close()
#elib.stopExp(sid,hz,size[0],size[1],seed,dbConf)


core.quit()
