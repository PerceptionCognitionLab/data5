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

scale=400

trialClock=core.Clock()

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)

#frameDurations=[82,82,6,0,100,6,6]

gParDict={"radius":150,
      "r":[125,140,160,175],
      "let":['X','M'],
      "mask":['@','#'],
      "abortKey":'9',
      "keyList":['x','m','9']
      }
gPar = SimpleNamespace(**gParDict)

lParDict={"cond":0,
          "angle":0,
          "target":0,
          "dur":100}
lPar = SimpleNamespace(**lParDict)

rng = random.default_rng()

def d2r(theta):
    return(math.radians(theta))

def getResp():
    keys=event.getKeys(keyList=gPar.keyList,timeStamped=trialClock)
    if len(keys)==0:
        keys=event.waitKeys(keyList=gPar.keyList,timeStamped=trialClock)
    resp=keys[0][0]
    rt=keys[0][1]
    if resp==gPar.abortKey:
        fptr.close()
        win.close()
        core.quit()   
    resp = int(resp==gPar.keyList[1])
    return([resp,round(rt,3)])

def runTrial(lPar):
    frames=[]
    frameDurations=[82,82,6,lPar.dur,100,6,6]
    #frameDurations[3]=lPar.dur

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
    return(ans)


def runBlock(blk):
    lPar.cond=1

    for trl in range(10):

        theta = rng.integers(0,360,1)
        lPar.angle=theta

        lPar.target = int(rng.integers(0,2,1))

        [resp,rt]=runTrial(lPar)

        if (resp==lPar.target)&(lPar.dur>0):
            lPar.dur = lPar.dur-20
        elif (resp==lPar.target)&(lPar.dur==0):
            lPar.dur=lPar.dur
        else:
            lPar.dur = lPar.dur+20

        print(pid,sid,blk,trl,lPar.cond,lPar.target,lPar.dur,resp,rt,sep=", ", file=fptr)



message=visual.TextStim(win,"Press a key to start")
message.draw()
win.flip()
event.waitKeys() 



runBlock(0)
win.close()
fptr.close
core.quit()

