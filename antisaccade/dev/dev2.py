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
      "keyList":['x','m','9']
      "posCue":[(-100,0),(100,0)]}
gPar = SimpleNamespace(**gParDict)

lParDict={"cond":0,
          "posTar":0,
          "target":0,
          "dur":100}
lPar = SimpleNamespace(**lParDict)

frameDurations=[82,82,6,lPar.dur,6,6,6]
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
    frameDurations[3]=lPar.dur

    #lPar.pos = int(rng.integers(0,2,1))
    #lPar.target = int(rng.integers(0,2,1))

    #if lPar.cond==1:
        #lPar.posCue=lPar.posTar*-1
    #else:
        #lPar.posCue=lPar.posTar
    
    
    fix=visual.TextStim(win,"+", height = 30)
    fixL=visual.Rect(win,width=30,height=30,pos=(-100,0),lineColor=(0.5,0.5,0.5))
    fixR=visual.Rect(win,width=30,height=30,pos=(100,0),lineColor=(0.5,0.5,0.5))
    cueL=visual.Rect(win,width=30,height=30,pos=(-100,0),lineColor=(1,1,1))
    cueR=visual.Rect(win,width=30,height=30,pos=(100,0),lineColor=(1,1,1))





    frames.append(visual.BufferImageStim(win,stim=(fix,fixL,fixR)))
    
    #frames.append(visual.TextStim(win,"+", height = 30))
    frames.append(visual.TextStim(win, " "))
    
    #cue
    
    #frames.append(visual.BufferImageStim(win,stim=(,)))
    
    #frames.append(visual.TextStim(win, " ")) #2-up/1-down
    #target
    #frames.append(visual.TextStim(win, gPar.let[lPar.target],pos=pos))
    #masks
    #frames.append(visual.TextStim(win, gPar.mask[0],pos=pos))
    #frames.append(visual.TextStim(win, gPar.mask[1],pos=pos))
    #stamps=el.runFrames(win,frames,frameDurations,trialClock)
    #ans=getResp()
    #return(ans)


#def runBlock(blk):
    #lPar.cond=1
    #numCor=0

    #for trl in range(2):

        #[resp,rt]=runTrial(lPar)
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


#runBlock(0)
runTrial(lPar)
win.close()
fptr.close
core.quit()

