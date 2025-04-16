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
from types import SimpleNamespace

pid=1
sid=1
fname="test"
fptr=open(fname,"w")
blk=0
trl=0

cond=0
theta=0
target=0

scale=400

trialClock=core.Clock()

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)

gParDict={"radius":150,
      "r":[125,140,160,175],
      "let":['X','M'],
      "mask":['@','#']}
gPar = SimpleNamespace(**gParDict)

lParDict={"cond":cond,
          "angle":theta,
          "target":target,
          "dur":60}
lPar = SimpleNamespace(**lParDict)


frameDurations=[82,82,49,lPar.dur,30,6,6]
rng = random.default_rng()

def d2r(theta):
    return(math.radians(theta))

def getResp(abortKey='9'):
    keys=event.getKeys(keyList=['x','m',abortKey],timeStamped=trialClock)
    if len(keys)==0:
        keys=event.waitKeys(keyList=('x','m',abortKey),timeStamped=trialClock)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==abortKey:
        fptr.close()
        win.close()
        core.quit()   
    resp = int(resp=='m')
    return([resp,rt])

def runTrial(lPar,trl):

    frames=[]
    if lPar.cond==1:
        cueAngle = (lPar.angle+180)%360
    else:
        cueAngle =  lPar.angle
    
    frames.append(visual.TextStim(win,"+", height = 30))
    frames.append(visual.TextStim(win, " "))
    #cue
    start0=[gPar.r[0]*math.cos(d2r(cueAngle)),gPar.r[0]*math.sin(d2r(cueAngle))]
    end0=[gPar.r[1]*math.cos(d2r(cueAngle)),gPar.r[1]*math.sin(d2r(cueAngle))]
    start1=[gPar.r[2]*math.cos(d2r(cueAngle)),gPar.r[2]*math.sin(d2r(cueAngle))]
    end1=[gPar.r[3]*math.cos(d2r(cueAngle)),gPar.r[3]*math.sin(d2r(cueAngle))]
    line0=visual.Line(win,start0,end0)
    line1=visual.Line(win,start1,end1)
    frames.append(visual.BufferImageStim(win,stim=(line0, line1)))
    frames.append(visual.TextStim(win, " ")) #2-up/1-down
    #target
    pos=(gPar.radius*math.cos(d2r(lPar.angle)),gPar.radius*math.sin(d2r(lPar.angle)))
    frames.append(visual.TextStim(win, gPar.let[lPar.target],pos=pos))
    #masks
    frames.append(visual.TextStim(win, gPar.mask[0],pos=pos))
    frames.append(visual.TextStim(win, gPar.mask[1],pos=pos))
    stamps=el.runFrames(win,frames,frameDurations,trialClock)
    ans=getResp()
    return(ans,trl)


def runBlock(blk):
    blk+=1

    cond = rng.integers(0,2,1)
    lPar.cond=cond

    for i in range(3):
        trl=i
        theta = rng.integers(0,360,1)
        lPar.angle=theta

        target = int(rng.integers(0,2,1))
        lPar.target=target

        ans=runTrial(lPar,trl)

        print(pid,sid,blk,trl,cond,gPar.let[lPar.target],lPar.dur,ans)

message=visual.TextStim(win,"Press a key to start")
message.draw()
win.flip()
event.waitKeys() 



runBlock(blk)
win.close()
fptr.close
core.quit()

