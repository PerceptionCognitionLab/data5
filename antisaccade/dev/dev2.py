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

lParDict={"isCongruent":0,
          "target":0,
          "posTarg":0,          
          "dur":20}
lPar = SimpleNamespace(**lParDict)

fixX=visual.TextStim(win,"+", height = 30)
fixL=visual.Rect(win,pos=gPar.pos[0],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
fixR=visual.Rect(win,pos=gPar.pos[1],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
cXLR=visual.BufferImageStim(win,stim=(fixX,fixL,fixR))
box=[fixL,fixR]


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


def condition():
    lPar.target = int(rng.integers(0,2,1))
    lPar.posTarg = int(rng.integers(0,2,1))  #0=left, 1=right
    if lPar.isCongruent==1:
        posCue=lPar.posTarg
    else:
        posCue=1-lPar.posTarg
    return(posCue)


def runTrial(lPar,posCue,cXLR):
    frames=[]
    frameDurations=[60,1,lPar.dur,5,5,5]

    #frame 0 START
    fixX=visual.TextStim(win,"+", height = 30)
    fixL=visual.Rect(win,pos=gPar.pos[0],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
    fixR=visual.Rect(win,pos=gPar.pos[1],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
    cXLR=visual.BufferImageStim(win,stim=(fixX,fixL,fixR))
    box=[fixL,fixR]
    frames.append(cXLR)
    #frame 1 CUE
    box[posCue].fillColor=[1,1,1]
    frames.append(visual.BufferImageStim(win,stim=box+[fixX]))
    box[posCue].fillColor=[-1,-1,-1]
    #frame 2 SAME AS START BUT 2-UP/1-DOWN
    frames.append(cXLR)
    #frame 3 TARGET
    targ=visual.TextStim(win, gPar.let[lPar.target],pos=gPar.pos[lPar.posTarg])
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,targ)))
    #frames 4/5 MASKS
    mask1=visual.TextStim(win, gPar.mask[0],pos=gPar.pos[lPar.posTarg])
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask1)))
    mask2=visual.TextStim(win, gPar.mask[1],pos=gPar.pos[lPar.posTarg])
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask2)))
    stamps=el.runFrames(win,frames,frameDurations,trialClock)
    ans=getResp()
    return(ans)


def runBlock(blk):
    blockStart(blk)
    condition()
    if (blk==0) | (blk==2) | (blk==4):
        lPar.isCongruent=1
    else:
        lPar.isCongruent=0

    lPar.dur=50
    numCor=0

    for trl in range(4):

        [resp,rt]=runTrial(lPar)
        print(pid,sid,blk,trl,lPar.isCongruent,lPar.target,lPar.dur,resp,rt,sep=", ", file=fptr)

        if (resp==lPar.target)&(numCor==0):
            numCor+=1
        elif (resp==lPar.target)&(numCor==1):
            lPar.dur = lPar.dur-3
            if lPar.dur<0:
                lPar.dur=0
            numCor=0
        else:
            lPar.dur = lPar.dur+3
            numCor=0


def blockStart(blk):
    messageText=f"Block {blk+1} \n\nPress key to start"
    message=visual.TextStim(win,messageText)
    message.draw()
    win.flip()
    event.waitKeys()

def intro():
    messageIntro=visual.TextStim(win,"Welcome to the experiment. \n\nWe will start with some training blocks.\n\nPress any key to begin training")
    messageIntro.draw()
    win.flip()
    event.waitKeys()

def t1(posCue):
    
    
    win.flip()
    event.waitKeys()

    t1=box[posCue].fillColor=[1,1,1]
    t1.draw
    
    box[posCue].fillColor=[-1,-1,-1]




def startExp():
    message=visual.TextStim(win,"Now we will start the experiment blocks. \n\nPress a key to continue.")
    message.draw()
    win.flip()
    event.waitKeys()



intro()
t1(condition())
startExp()
blocks=[0,1,2,3,4,5]
for i in range(int(len(blocks))): 
    blk=blocks[i]
    runBlock(blk)
win.close()
fptr.close
core.quit()

