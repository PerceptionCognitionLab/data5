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

gPar={"radius":150,
      "r":[125,140,160,175],
      "let":['X','M'],
      "mask":['@','#']}


frames=[]
# frameDurations=[82,82,49,2,30,6,6]
frameDurations=[100,100,100,0,100,100,100]

rng = random.default_rng()
theta=0
cond=0 
target=0

def d2r(theta):
    return(math.radians(theta))

lPar={"cond":cond,"angle":theta,"target":target,"dur":200}


def runTrial(lPar):

    if lPar["cond"]==1:
        cueAngle = (lPar["angle"]+180)%360
    else:
        cueAngle =  lPar["angle"]
    
    frameDurations[3]=lPar["dur"]
    frames.append(visual.TextStim(win,"+", height = 30))
    frames.append(visual.TextStim(win, "BLANK"))
    #cue
    start0=[gPar["r"][0]*math.cos(d2r(cueAngle)),gPar["r"][0]*math.sin(d2r(cueAngle))]
    end0=[gPar["r"][1]*math.cos(d2r(cueAngle)),gPar["r"][1]*math.sin(d2r(cueAngle))]
    start1=[gPar["r"][2]*math.cos(d2r(cueAngle)),gPar["r"][2]*math.sin(d2r(cueAngle))]
    end1=[gPar["r"][3]*math.cos(d2r(cueAngle)),gPar["r"][3]*math.sin(d2r(cueAngle))]
    line0=visual.Line(win,start0,end0)
    line1=visual.Line(win,start1,end1)
    frames.append(visual.BufferImageStim(win,stim=(line0, line1)))
    frames.append(visual.TextStim(win, "BLANK2")) #2-up/1-down
    #target
    pos=(gPar["radius"]*math.cos(d2r(lPar["angle"])),gPar["radius"]*math.sin(d2r(lPar["angle"])))
    frames.append(visual.TextStim(win, gPar["let"][lPar["target"]],pos=pos))
    #masks
    frames.append(visual.TextStim(win, gPar["mask"][0],pos=pos))
    frames.append(visual.TextStim(win, gPar["mask"][1],pos=pos))
    stamps=el.runFrames(win,frames,frameDurations,trialClock)
    #event.waitKeys()


def runBlock(cond):
    for i in range(2):
        theta = rng.integers(0,360,1)
        lPar["angle"]=theta

        cond = rng.integers(0,2,1)
        lPar["cond"]=cond

        target = 0 #rng.integers(0,2,1)
        lPar["target"]=target
        
        
        #lPar["dur"]=
        
        runTrial(lPar)




#message=visual.TextStim(win,"Press a key to start")
#message.draw()
#win.flip()
#event.waitKeys() 



runBlock(0)
win.close()

# print("Difference Between Time Stamps:\n",np.diff(stamps),"\n")
# print("Difference Between Frames:\n",el.actualFrameDurations(frameDurations,stamps))
core.quit()

