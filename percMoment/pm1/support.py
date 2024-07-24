from psychopy import core, visual, sound, event, clock
import random
import numpy as np


correct1 = sound.Sound(500,secs = .1) # correct response
correct2 = sound.Sound(1000,secs = .2)

def feedback(correct):
	if correct:
		correct1.play()
		correct2.play()

def initGlobals(gPar0):

	def makeCoord(size,spacing):
		x = []
		y = []
		for i in range(size*size):
			result = divmod(i, size)
			x.append(spacing * (result[0] - (size-1)/2))
			y.append(spacing * (result[1] - (size-1)/2))
		return([x,y])

	def makeValidTarget(sizeIndicator):
		validTarget=[]
		size=len(sizeIndicator)
		for i in range(size*size):
			result=divmod(i, size)
			if sizeIndicator[result[0]] ==1 and sizeIndicator[result[1]] ==1:
				validTarget.append(i)
		return(validTarget)

	gPar=gPar0
	gPar['size']=len(gPar['sizeIndicator'])
	[x,y]=makeCoord(gPar['size'],gPar['spacing'])
	gPar['x']=x
	gPar['y']=y
	gPar['validTarget']=makeValidTarget(gPar['sizeIndicator'])
	gPar['N']=len(x)
	return(gPar)

def mouseNext(mouse):
	mousePress = False
	while True:
		if mouse.getPressed()[2]:  
			break


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

def mouseResponse(mouse,win,gPar,frame):
	[x,y]=[gPar['x'],gPar['y']]
	mousePress = False
	mouse.setVisible(True)
	mouse.setPos((300,0))
	while not mousePress:
		buttons = mouse.getPressed(getTime=False)
		resp = mouseOnResp(x, y, mouse.getPos())
		frame.draw()
		if resp > -1: 
			respDot = visual.Circle(win, pos=(x[resp], y[resp]), fillColor=[1, 1, 1], radius=2)
			respDot.draw()
		win.flip()
		mousePress = any(buttons)
	mouse.setVisible(False)
	return(resp)

def intDotIndex(gPar,target):
    s2=gPar['N']
    half=int((s2-1)/2)
    tot = np.array(range(s2))
    wot = np.delete(tot, target)
    index = np.array(range(s2-1))
    iA = np.sort(np.random.choice(index, half, replace=False))
    iB = np.delete(index, iA)
    return [wot[iA], wot[iB]]

def stairCase(soa,correct,correctPrevious,increment):
	if (correct and correctPrevious==1):
		soa+=increment
		cv=0
	if (correct and correctPrevious==0):
		cv=1   
	if (not correct):
		soa+= (-increment)
		cv=0
	if (soa==0):
		soa=1
	return ([soa,cv]) 

def maskStairCase(soa,correct,correctPrevious,increment):
	if (correct or not correct):
		soa = soa - 1
		cv = 0
	if (soa==0):
		soa=1
	return ([soa,cv]) 

def instruct(win, mouse,message,advance='mouse'):

	text_height = 35  
	line_spacing = 1.5  
	lines = message.split('\n')

	core.wait(.3)
	for i, line in enumerate(lines):
		y_position = (len(lines) * text_height * line_spacing / 2) - (i * text_height * line_spacing) 
		visual.TextStim(win, text=line, height=text_height, pos=(0, y_position)).draw()
	win.flip()
	if advance== 'mouse':
		mouseNext(mouse);
	else:
		event.waitKeys()
	return 0