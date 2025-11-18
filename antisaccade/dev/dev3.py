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

#expName="dev3"
refreshRate=165
seed= -1

#dbConf=el.beta
#el.setRefreshRate(refreshRate)
#[pid,sid,fname]=el.startExp(expName,dbConf,pool=1,lockBox=False,refreshRate=refreshRate)

fptr=open(fname,"w")
rng = random.default_rng()

scale=400

trialClock=core.Clock()
correctSound1 = sound.Sound(500, secs=0.25)
correctSound2 = sound.Sound(1000, secs=0.25)
errorSound1 = sound.Sound(500, secs=0.5)
errorSound2 = sound.Sound(375, secs=0.5)

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)

gParDict={"let":['A','S','D','F','G','H','J','K','L'],
      "mask":['@','#'],
      "abortKey":'9',
      "keyList":['a','s','d','f','g','h','j','k','l','9'],
      "pos":[(-400,0),(400,0)],
      "numTrials":10}
gPar = SimpleNamespace(**gParDict)

targDur=2
lParDict={"isCongruent":0,
          "target":0,
          "posTarg":0,          
          "dur":[50,2,0,16,16,16]}
lPar = SimpleNamespace(**lParDict)

def createStim():
    fixX=visual.TextStim(win,"+", height = 30)
    fixL=visual.Rect(win,pos=gPar.pos[0],fillColor=(-1,-1,-1),lineColor=(0,0,0),lineWidth=2,width=50,height=60)
    fixR=visual.Rect(win,pos=gPar.pos[1],fillColor=(-1,-1,-1),lineColor=(0,0,0),lineWidth=2,width=50,height=60)
    cXLR=visual.BufferImageStim(win,stim=(fixX,fixL,fixR))
    box=[fixL,fixR]
    targ=visual.TextStim(win, gPar.let[lPar.target],pos=gPar.pos[lPar.posTarg])
    mask1=visual.TextStim(win, gPar.mask[0],pos=gPar.pos[lPar.posTarg])
    mask2=visual.TextStim(win, gPar.mask[1],pos=gPar.pos[lPar.posTarg])
    return fixX,fixL,fixR,cXLR,box,targ,mask1,mask2

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
    resp = gPar.keyList.index(resp)
    return([resp,round(rt,3)])



def runTrial():
    frames=[]


    if lPar.isCongruent==1:
        posCue=lPar.posTarg
    else:
        posCue=1-lPar.posTarg
    
    fixX,fixL,fixR,cXLR,box,targ,mask1,mask2=createStim()
    frames.append(cXLR)
    box[posCue].lineColor=[1,1,1]
    box[posCue].lineWidth=10
    frames.append(visual.BufferImageStim(win,stim=box+[fixX]))
    box[posCue].lineColor=[0,0,0]
    box[posCue].lineWidth=2
    frames.append(cXLR)
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,targ)))
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask1)))
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask2)))
    stamps=el.runFrames(win,frames,lPar.dur,trialClock)
    [resp,rt]=getResp()
    if (resp==lPar.target):
        correctSound1.play()
        correctSound2.play()
    else:
        errorSound1.play()
        errorSound2.play()

    return([resp,rt])
    

def runBlock(blk,cong,nTrials,increment=2):
    lPar.isCongruent=cong
    numCor=0
    for trl in range(nTrials):
        lPar.target = int(rng.integers(0,9,1))
        lPar.posTarg = int(rng.integers(0,2,1))  #0=left, 1=right
        [resp,rt]=runTrial()
        print(pid,sid,blk,trl,lPar.isCongruent,lPar.target,lPar.dur[targDur],resp,rt,sep=", ", file=fptr)
        print(pid,sid,blk,trl,lPar.isCongruent,lPar.target,lPar.dur[targDur],resp,rt)
    
        if (resp==lPar.target)&(numCor==0):
            numCor+=1
        elif (resp==lPar.target)&(numCor==1):
            lPar.dur[targDur] = lPar.dur[targDur]-increment
            if lPar.dur[targDur]<0:
                lPar.dur[targDur]=0
            numCor=0
        else:
            lPar.dur[targDur]=lPar.dur[targDur]+increment
            numCor=0

    return(lPar.dur[targDur])


last=[100,100]


#Block 0
cong=1
lPar.dur=[50,20,last[cong],20,16,16]
last[cong]=runBlock(0,cong,1)
#Block 1
cong=0
lPar.dur=[50,20,last[cong],20,16,16]
last[cong]=runBlock(1,cong,1)
#Block 2
last=[80,50]
cong=1
lPar.dur=[50,20,last[cong],20,16,16]
last[cong]=runBlock(2,cong,5,increment=5)

print(last)    
#hz=round(win.getActualFrameRate())
#[resX,resY]=win.size
win.close()
fptr.close
#el.stopExp(sid,hz,resX,resY,seed,dbConf)
core.quit()

