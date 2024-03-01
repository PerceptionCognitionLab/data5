from psychopy import core, visual, sound, event, clock
import math 
import random
import decimal
import sys
import numpy as np  
import os
import time

scale = 250

win = visual.Window(units="pix", size=(2 * scale, 2 * scale), color=[-1, -1, -1], fullscr=True)

def runFrames(frame,frameTimes):
        event.clearEvents()
        currentFrame=0
        cumTimes=np.cumsum(frameTimes)
        stamp=np.empty(max(cumTimes)+1)
        win.flip
        stamp[0]=clock.getTime()
        for refresh in range(max(cumTimes)):
                if refresh in cumTimes:
                        currentFrame=currentFrame+1
                frame[currentFrame].draw()
                win.flip()
                stamp[refresh+1]=clock.getTime()
        ds=np.diff(stamp)
        return(ds)


def makeDotIndex(target):
    tot=np.array(range(49))
    wot=np.delete(tot,target)
    index=np.array(range(48))
    iA=np.sort(np.random.choice(index,24,replace=False))
    iB=np.delete(index,iA)
    return([wot[iA],wot[iB]])

spacing=48
radius=4

#Tones
Tone_A = sound.Sound(3000,secs = 2)
Tone_B = sound.Sound(750,secs = 2)


fix=visual.TextStim(win,"+")
blank=visual.TextStim(win,"")

x=[]
y=[]

for i in range(49):
    result=divmod(i,7)
    x.append(spacing*(result[0]-3))
    y.append(spacing*(result[1]-3))

perimeter = [0,1,2,3,4,5,6,7,13,14,20,21,27,28,34,35,41,42,43,44,45,46,47,48]
valid_points = [i for i in range(49) if i not in perimeter]
target = random.choice(valid_points)
[aDots,bDots]=makeDotIndex(target)

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
    dots.append(visual.Circle(win, pos=(x[i],y[i]), fillColor=[0, -1, -1], radius=2))
all=visual.BufferImageStim(win,stim=dots)

frame=[]
frameTimes=[60,60,1,2,1,60,1]
frame.append(fix)
frame.append(blank)
frame.append(a)
frame.append(blank)
frame.append(b)
frame.append(blank)
frame.append(all)

d=runFrames(frame,frameTimes)

mouse = event.Mouse(visible=True, newPos=[0,0], win=win)




#def distAll(x,y,mousePos):
#    for i in range(len(x))



clicked_position = None
while clicked_position is None:
	buttons, times = mouse.getPressed(getTime=True)
	if any(buttons):
		clicked_position = mouse.getPos()

x_target = x[target]
y_target = y[target]

distance_from_target = np.sqrt((clicked_position[0] - x_target)**2 + (clicked_position[1] - y_target)**2)
critical_distance = 40 
correct = distance_from_target < critical_distance
    
#audio feedback

if correct:
    Tone_A.play()
else:
    Tone_B.play()

print("")
print("Correct:", correct)
print("Clicked position:", clicked_position)
print("Target location:",(x_target,y_target))
print("Target point:", target)
print("")
		
	
win.close()
core.quit()

