from psychopy import prefs
prefs.hardware['audioLib']=['PTB']
prefs.hardware['audioLatencyMode']=3
from psychopy import core, visual, sound, event
import numpy as np
from numpy import random
import sys
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
frameDurations=[30,30,30]

rng = random.default_rng()
stim1 = 0
n = rng.integers(0,2,1)
if n == 0:
    stim1 = 'M'
else:
    stim1 = 'X'

frames.append(visual.TextStim(win,"+"))
frames.append(visual.TextStim(win,stim1))
frames.append(visual.TextStim(win,"#"))

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
