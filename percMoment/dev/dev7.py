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

fix = visual.TextStim(win, "+")  # fixation cross
blank = visual.TextStim(win, "")  # blank window
int_trial = 3
mask_trial = 3

gPar0={
	'spacing' : 48,
	'sizeIndicator' : [0,1,1,1,0],
	'increment': [1,-1]
}  


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


def maskingTrial(soa,gPar):
	[x,y]=[gPar['x'],gPar['y']]
	target= random.choice(gPar['validTarget'])
	maskDots=[]
	redDots=[]
	targetDots=[]
	targetDots.append(visual.Circle(win, pos=(x[target],y[target]),fillColor=[1, 1, 1], radius=5))
	for i in range(gPar['N']):
		if (i != target):
			targetDots.append(visual.Circle(win, pos=(x[i],y[i]), fillColor=[0, -1, -1], radius=2.5))
		redDots.append(visual.Circle(win, pos=(x[i],y[i]), fillColor=[0, -1, -1], radius=2.5))
		maskDots.append(visual.Circle(win, pos=(x[i],y[i]),fillColor=[1, 1, 1], radius=5))
	allRed=visual.BufferImageStim(win,stim=redDots)
	mask=visual.BufferImageStim(win,stim=maskDots)
	targ=visual.BufferImageStim(win,stim=targetDots)
	frame = [fix, blank, targ, blank, mask, blank, allRed]
	frameDurations = [120, 60, 5, soa, 5, 60, 1]
	stamps=elib.runFrames(win,frame,frameDurations,trialClock)
	critTime=elib.actualFrameDurations(frameDurations,stamps)[3]
	critPass=(np.absolute(soa/refreshRate-critTime)<.001)
	resp=support.mouseResponse(mouse,win,gPar,frame[6])
	correct=target==resp
	support.feedback(correct)
	return([target,resp,correct,np.round(critTime,4),critPass])

def block(blk,task,trials,soa,gPar):
	correctPrevious=0 
	for t in range(trials):
		input=[pid,sid,blk,task,t,soa]
		if (task==0):
			result=integrationTrial(soa,gPar)
		if (task==1):
			result=maskingTrial(soa,gPar)
		output=input+result
		print(*output,sep=", ", file=fptr)
		[soa,correctPrevious]=support.stairCase(soa,result[2],correctPrevious,gPar['increment'][task])
	return(soa)


#########
		

gPar=support.initGlobals(gPar0)  # adds x, y, validTarget, N to structure


support.instruct(win,"Welcome")
support.instruct(win,"Integration Practice Task")
for r in range(int_trial):
	integrationTrial(1,gPar,prac=True)
support.instruct(win,"Masking Practice Task")
for r in range(mask_trial):
	maskingTrial(100,gPar)
for r in range(mask_trial):
	maskingTrial(80,gPar)
support.instruct(win,"Integration Task")
#block(0,1,3,60,gPar)
support.instruct(win,"Masking Task")
#block(0,0,3,1,gPar)

win.close()

core.quit()
