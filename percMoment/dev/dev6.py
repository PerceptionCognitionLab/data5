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
refreshRate=165
elib.setRefreshRate(refreshRate)
expName="pm1"
dbConf=elib.beta
#[pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
fname='test'
pid=1
sid=1
fptr=open(fname,"w")
 

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
mouse = event.Mouse(visible=False, newPos=[0,0], win=win) #mouse centered at zero
trialClock=core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)
abortKey=['9']
correct1 = sound.Sound(500,secs = .1) # correct response
correct2 = sound.Sound(1000,secs = .2)
def correctSound(correct):
	if correct:
		correct1.play()
		correct2.play()

# Display Parameter
spacing = 48 # spacing between dots
size=5

# Trial Settings
practice = 1 # number of practice trails
numTrials = 2 # number of trials
global correctPrevious

# Helpers
fix = visual.TextStim(win, "+")  # fixation cross
blank = visual.TextStim(win, "")  # blank window


# All Tasks

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

# Integration Staircase
def intAdjustSOA(soa,correct,correctPrevious):
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

# Differentiation Staircase
def difAdjustSOA(soa,correct,correctPrevious):
    if (correct and correctPrevious==1):
        soa-=2
        cv=0
    if (correct and correctPrevious==0):
    	cv=1   
    if (not correct):
        soa+=1
        cv=0
    if (soa==0):
     	soa=1
    return ([soa,cv]) 

def makeCoord(size,spacing):
    x = []
    y = []
    for i in range(size*size):
        result = divmod(i, size)
        x.append(spacing * (result[0] - (size-1)/2))
        y.append(spacing * (result[1] - (size-1)/2))
    return([x,y])

#integration practice
def IntmakePracticeDotIndex(missingDot):
    s2 = size * size
    tot = np.array(range(size*size))
    wot = np.delete(tot, missingDot)
    index = np.array(range(s2-1))
    empty = np.sort(np.random.choice(index, s2-1, replace=False))
    return [wot[empty]]

def IntpracticeTrial():
    target = random.choice(range(size*size))
    missingDot = random.choice(range(size*size))
    [pDots] = IntmakePracticeDotIndex(missingDot)
    x,y=makeCoord(size,spacing)
    dots=[]
    for i in range(len(pDots)):
	    dots.append(visual.Circle(win, pos=(x[pDots[i]],y[pDots[i]]), fillColor=[1, 1, 1], radius=5))
    p=visual.BufferImageStim(win,stim=dots)
    dots=[]
    for i in range(len(x)):
         dots.append(visual.Circle(win, pos=(x[i],y[i]), fillColor=[0, -1, -1], radius=2.5))
    all=visual.BufferImageStim(win,stim=dots)	
    frame = [fix, p ,all]
    frameDurations = [120,60,1]
    stamps=elib.runFrames(win,frame,frameDurations,trialClock)		
    mousePress = False
    mouse.setVisible(True)
    mouse.setPos((300,0))
    while not mousePress:
        buttons = mouse.getPressed(getTime=False)
        resp = mouseOnResp(x, y, mouse.getPos())
        frame[2].draw()
        if resp > -1: 
            respDot = visual.Circle(win, pos=(x[resp], y[resp]), fillColor=[1, 1, 1], radius=2)
            respDot.draw()
        win.flip()
        mousePress = any(buttons)
# Give Feedback
    correct = resp == missingDot
    correctSound(correct)
    mouse.setVisible(False)

def DifmakePracticeDotIndex(target,size):
    s2=size*size
    tot = np.array(range(s2))
    return [target, tot]

#Differentiation Practice
def DifpracticeTrial():
    target = random.choice(range(size*size))
    [x,y]=makeCoord(size,spacing)
    aDots = [target]
    bDots = list(range(size*size))
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
    frameDurations = [120, 5, 100, 30, 80, 5, 1]
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
#   Give Feedback
    correct = resp == target
    correctSound(correct)
    mouse.setVisible(False)

# Integrate Task
    
def makeDotIndex(task,target,size):
    if (task==0): 
        [wA,wB]=intMakeDotIndex(target,size)
    if (task==1):
         [wA,wB]=diffMakeDotIndex(target,size)
    return([wA,wB])

def diffMakeDotIndex(target,size):
    s2=size*size
    tot = np.array(range(s2))
    return [target, tot]

def intMakeDotIndex(target,size):
    s2=size*size
    half=int((s2-1)/2)
    tot = np.array(range(s2))
    wot = np.delete(tot, target)
    index = np.array(range(s2-1))
    iA = np.sort(np.random.choice(index, half, replace=False))
    iB = np.delete(index, iA)
    return [wot[iA], wot[iB]]

def doTrial(soa, task, size, correctPrevious):
    target = random.choice(range(size*size))
    [x,y]=makeCoord(size,spacing)
    dots=[]
    for i in range(len(x)):
        dots.append(visual.Circle(win, pos=(x[i],y[i]), fillColor=[0, -1, -1], radius=2.5))
    all=visual.BufferImageStim(win,stim=dots)
    if task == 0:
        [aDots, bDots] = makeDotIndex(task,target,size)
    elif task == 1:
         aDots = [target]
         bDots = list(range(size*size))
    dots=[]
    for i in range(len(aDots)):
        dots.append(visual.Circle(win, pos=(x[aDots[i]],y[aDots[i]]), fillColor=[1, 1, 1], radius=5))
    a=visual.BufferImageStim(win,stim=dots)
    dots=[]
    for i in range(len(bDots)):
        dots.append(visual.Circle(win, pos=(x[bDots[i]],y[bDots[i]]), fillColor=[1, 1, 1], radius=5))
    b=visual.BufferImageStim(win,stim=dots)
    frame = [fix, blank, a, blank, b, blank, all]
    frameDurations = [120, 60, 5, soa, 5, 60, 1]
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
    print(soa, target, resp, correct, correctPrevious)
    fptr.flush()
    mouse.setVisible(False)
    # task 0=integration, 1 = differentiation
    if task == 0: 
         soa, correctPrevious = intAdjustSOA(soa, correct, correctPrevious)
    elif task == 1: 
         soa, correctPrevious = difAdjustSOA(soa, correct, correctPrevious)

    return correct, soa, correctPrevious 

def instruct(win, message):
    text_height = 35  
    line_spacing = 1.5  
    lines = message.split('\n')

    for i, line in enumerate(lines):
        y_position = (i * text_height * line_spacing) - (len(lines) * text_height * line_spacing / 2)
        visual.TextStim(win, text=line, height=text_height, pos=(0, y_position)).draw()

    win.flip()
    event.waitKeys()
    return 0



############################################################################33
##   Begin Experiment Here 


instruct(win,"Welcome")

instruct(win,"Integration practice task Here, you will see a fixation cross followed by a matrix. Select the space with the missing dot. Press any key to continue")

for i in range(practice):
	correct=IntpracticeTrial()
     
instruct(win, "Differentiation practice task: Here, you will see a fixation cross followed by a matrix. Select the space where you saw the single dot. press any key to continue")

for i in range(practice):
	correct=DifpracticeTrial()

instruct(win,"Just like in the practice trial, you will see a fixation cross followed by a matrix. Select the space with the missing dot. Press any key to begin trials")

soa = 1
correctPrevious = 0

for n in range(numTrials):
    task = 0
    correct, soa, correctPrevious = doTrial(soa, task, size, correctPrevious)
  
instruct(win,"This is the differentiation task. Here, you will see a fixation cross followed by a matrix. Select the space with the missing dot. Press any key to begin trials")

soa = 20
# Differentiation Task
for n in range(numTrials):
    task = 1
    correct, soa, correctPrevious = doTrial(soa, task, size, correctPrevious)

instruct(win,"Thank You")

exit()

win.close()
elib.stopExp(sid,hz,size[0],size[1],seed,dbConf)


core.quit()



#########################################################################################################################

