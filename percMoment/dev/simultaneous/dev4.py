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
import support


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
correctSound1=sound.Sound(value=500,secs=.1)
correctSound2=sound.Sound(value=1000,secs=.2)
errorSound=sound.Sound(value=300,secs=.5)
seed = random.randrange(1e6)
random.seed(seed)

fix = visual.TextStim(win, "+")  # fixation cross
gPar0={
	'spacing' : 48,
	'sizeIndicator' : [0,1,1,1,0],
	'increment': [1,-1]
}  
gPar=support.initGlobals(gPar0)  # adds x, y, validTarget, N to structure
fix = visual.TextStim(win, "+")  # fixation cross
blank = visual.TextStim(win, "")  # blank window
int_trial = 3


#############
# simultaneous task trial
#############

def runTrial(dur, stimCode):
    stim=[]
    stim.append(visual.Circle(win, pos=(-96,0.0), fillColor=[1, 1, 1], radius=4))
    stim.append(visual.Circle(win, pos=(96,0.0), fillColor=[1, 1, 1], radius=4))
    both=visual.BufferImageStim(win,stim=stim)
    stim.append(both)
    blank = visual.TextStim(win, '', pos = (0.0,0.0))
    option = []
    option.append(visual.TextBox2(win, text = "Simultaneous", size=(1.8,.1), pos=(-480,-96)))
    option.append(visual.TextBox2(win, text = "Non-Simultaneous", size=(1.8,.1), pos=(360,-96)))
    options=visual.BufferImageStim(win,stim=option)
    easy=visual.TextStim(win,"help")

    frames = [blank, stim[stimCode], blank, both, options]
    frameTimes = [100, 1, dur, 1, 100]
    stamps=elib.runFrames(win, frames, frameTimes, trialClock, addBlank=False)
    event.waitKeys()
    exit(1)
    keys = event.waitKeys(timeStamped=trialClock, 
                          keyList=['x', 'm', '9'])
    resp=1
    if keys[0][0]=='x':
        resp=0
    return(resp)
    # resp "1/m" means same and "0/x" is different

#############
# fusion task trial
#############

def integrationTrial(soa,gPar,prac=False):
	[x,y]=[gPar['x'],gPar['y']]
	target= random.choice(gPar['validTarget'])
	[aDots, bDots]=support.intDotIndex(gPar,target)
	dots=[]
	for i in range(gPar['N']):
		dots.append(visual.Circle(win, pos=(x[i],y[i]), fillColor=[0, -1, -1], radius=2.5))
	allRed=visual.BufferImageStim(win,stim=dots)
	adots=[]
	alldots=[]
	for i in range(len(aDots)):
		adots.append(visual.Circle(win, pos=(x[aDots[i]],y[aDots[i]]), fillColor=[1, 1, 1], radius=5))
		alldots.append(visual.Circle(win, pos=(x[aDots[i]],y[aDots[i]]), fillColor=[1, 1, 1], radius=5))
	a=visual.BufferImageStim(win,stim=adots)
	bdots=[]
	for i in range(len(bDots)):
		bdots.append(visual.Circle(win, pos=(x[bDots[i]],y[bDots[i]]), fillColor=[1, 1, 1], radius=5))
		alldots.append(visual.Circle(win, pos=(x[bDots[i]],y[bDots[i]]), fillColor=[1, 1, 1], radius=5))
	b=visual.BufferImageStim(win,stim=bdots)
	frame = [fix, blank, a, blank, b, blank, allRed]
	frameDurations = [120, 60, 5, soa, 5, 60, 1]
	if prac:
			all=visual.BufferImageStim(win,stim=alldots)
			frame = [fix,blank,all,blank,blank,blank,allRed]
			frameDurations=[120,60,120,1,1,60,1]
	stamps=elib.runFrames(win,frame,frameDurations,trialClock)
	critTime=elib.actualFrameDurations(frameDurations,stamps)[3]
	critPass=(np.absolute(soa/refreshRate-critTime)<.001)
	resp=support.mouseResponse(mouse,win,gPar,frame[6])
	correct=target==resp
	support.feedback(correct)
	return([target,resp,correct,np.round(critTime,4),critPass])


#############
# staircase
#############
def runSimult(trialNum):
    counter = 0
    dur = 6
    for i in range(trialNum):
        trialNum = i
        stim = random.choice([0,1,2])
        resp=runTrial(dur,stim)
        info=[trialNum, dur, stim, resp]
        if info[2]==2:
            info[2] = 1
        else:
            info[2] = 0
        print(*info, sep=' ', file=fptr)
        # staircase
        if (info[2]==info[3])&(counter==0):
            counter+=1
            support.feedback("correct")
        elif (info[2]==info[3])&(counter==1):
            support.feedback("correct")
            dur = dur-2
            if dur<0:
                dur=0
            counter=0
        else:
            dur = dur+2
            if dur>8:
                dur=8
            counter=0

def runInteg(trialNum):
    counter = 0
    soa = 6
    for i in range(trialNum):
        trialNum = i
        resp=integrationTrial(soa,gPar,prac=False)
        print("target,resp,correct",resp[0],resp[1],resp[2])
        info=[trialNum, soa, resp[2]]
        print(*info, sep=' ', file=fptr)
        # staircase
        if (info[2]==True)&(counter==0):
            counter+=1
        elif (info[2]==True)&(counter==1):
            soa = soa+2
            if soa>8:
                soa=8
            counter=0
            
        else:
            soa = soa-1
            if soa<0:
                soa=0
            counter=0
        

#############


#runInteg(10)
runSimult(2)
support.instruct(win,"Welcome")
support.instruct(win,"Integration Task")
runInteg(0)
support.instruct(win,"Simultaneous Task")
runSimult(2)


fptr.close()
win.close()
core.quit()