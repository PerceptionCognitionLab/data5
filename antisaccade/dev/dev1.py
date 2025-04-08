from psychopy import prefs  
prefs.hardware['audioLib']=['PTB']
prefs.hardware['audioLatencyMode']=3
from psychopy import core, visual, sound, event
import numpy as np
from numpy import random
import sys
import math
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as el


scale=400

trialClock=core.Clock()

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)


frames=[]
frameDurations=[82,82,49,2,30,6,6]

rng = random.default_rng()

#stimulus
stim1 = 0
stim = rng.integers(0,2,1)
if stim == 0:
    stim1 = 'M'
else:
    stim1 = 'X'

#stim angle
degAngle = rng.integers(0,360,1)
radAngle = math.radians(degAngle)
xpos = 300*math.cos(radAngle)
ypos = 300*math.sin(radAngle)

#condition
cond=0
pickCond=rng.integers(0,2,1)
#congruent condition
if pickCond == 0: 
    xcue = 300*math.cos(radAngle)
    ycue = 300*math.sin(radAngle)
#incongruent condition 
else:
    xcue = -300*math.cos(radAngle)
    ycue = -300*math.sin(radAngle) 

cue1 = visual.Line(win, start=(xcue,ycue+10), end=(xcue,ycue+2)) #arbitraty location, just trying to get them to present simultaneously 
cue2 = visual.Line(win, start=(xcue,ycue-10), end=(xcue,ycue-2))

frames.append(visual.TextStim(win,"+", height = 30))
frames.append(visual.TextStim(win, " "))
frames.append(visual.BufferImageStim(win, stim(cue1,cue2)))
frames.append(visual.TextStim(win, " "))
frames.append(visual.TextStim(win,stim1, pos=(xpos, ypos), height=30))
frames.append(visual.TextStim(win,"#", pos=(xpos,ypos), height=30))
frames.append(visual.TextStim(win, "@", pos=(xpos,ypos), height=30)) 

message=visual.TextStim(win,"Press a key to start")
message.draw()
win.flip()
event.waitKeys() 

stamps=el.runFrames(win,frames,frameDurations,trialClock)

event.waitKeys()
win.close()

print("Difference Between Time Stamps:\n",np.diff(stamps),"\n")
print("Difference Between Frames:\n",el.actualFrameDurations(frameDurations,stamps))
core.quit()

