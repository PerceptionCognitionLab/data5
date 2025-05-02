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

gParDict={"let":['X','M'],
      "mask":['@','#'],
      "abortKey":'9',
      "keyList":['x','m','9'],
      "pos":[(-200,0),(200,0)]}
gPar = SimpleNamespace(**gParDict)

lParDict={"cond":0,
          "target":0,
          "dur":100}
lPar = SimpleNamespace(**lParDict)

rng = random.default_rng()

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
    frameDurations=[10,20,lPar.dur,20,20,20]
    frameDurations[3]=lPar.dur

    lPar.target = int(rng.integers(0,2,1))

    
    #frame 1 START
    fixX=visual.TextStim(win,"+", height = 30)
    fixL=visual.Rect(win,pos=gPar.pos[0],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
    fixR=visual.Rect(win,pos=gPar.pos[1],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR)))
    #frame 2 CUE
    cue=visual.Rect(win,pos=gPar.pos[0],fillColor=(1,1,1),width=50,height=60)
    frames.append(visual.BufferImageStim(win,stim=(cue,fixX,fixL,fixR)))
    #frame 3 SAME AS START BUT 2-UP/1-DOWN
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR)))
    #frame 4 TARGET
    targ=visual.TextStim(win, gPar.let[lPar.target],pos=gPar.pos[0])
    frames.append(visual.BufferImageStim(win,stim=(targ,fixX,fixL,fixR)))
    #frames 5/6 MASKS
    mask1=visual.TextStim(win, gPar.mask[0],pos=gPar.pos[0])
    frames.append(visual.BufferImageStim(win,stim=(mask1,fixX,fixL,fixR)))
    mask2=visual.TextStim(win, gPar.mask[1],pos=gPar.pos[0])
    frames.append(visual.BufferImageStim(win,stim=(mask2,fixX,fixL,fixR)))
    stamps=el.runFrames(win,frames,frameDurations,trialClock)
    ans=getResp()
    return(ans)


def runBlock(blk):
    lPar.cond=0
    #numCor=0

    for trl in range(1):

        [resp,rt]=runTrial(lPar)
        #print(pid,sid,blk,trl,lPar.cond,lPar.target,lPar.dur,resp,rt,sep=", ", file=fptr)

        #if (resp==lPar.target)&(numCor==0):
            #numCor+=1
        #elif (resp==lPar.target)&(numCor==1):
            #lPar.dur = lPar.dur-3
            #if lPar.dur<0:
                #lPar.dur=0
            #numCor=0
        #else:
            #lPar.dur = lPar.dur+3
            #numCor=0



message=visual.TextStim(win,"Press a key to start")
message.draw()
win.flip()
event.waitKeys()


runBlock(1)
runTrial(lPar)
win.close()
fptr.close
core.quit()

