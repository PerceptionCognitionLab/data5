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
rng = random.default_rng()

scale=400

trialClock=core.Clock()

win=visual.Window(units= "pix", 
                     allowGUI=False,
                     size=(2*scale,2*scale),
                     color=[-1,-1,-1],
                     fullscr = True)

gParDict={"let":['A','S','D','F','G','H','J','K','L'],
      "mask":['@','#'],
      "abortKey":'9',
      "keyList":['a','s','d','f','g','h','j','k','l','9'],
      "pos":[(-200,0),(200,0)]}
gPar = SimpleNamespace(**gParDict)

lParDict={"isCongruent":0,
          "target":0,
          "posTarg":0,          
          "dur":20}
lPar = SimpleNamespace(**lParDict)

def createStim():
    fixX=visual.TextStim(win,"+", height = 30)
    fixL=visual.Rect(win,pos=gPar.pos[0],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
    fixR=visual.Rect(win,pos=gPar.pos[1],fillColor=(-1,-1,-1),lineColor=(0,0,0),width=50,height=60)
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

def runTrial(lPar):
    frames=[]
    frameDurations=[60,1,lPar.dur,5,5,5]

    lPar.target = int(rng.integers(0,9,1))
    lPar.posTarg = int(rng.integers(0,2,1))  #0=left, 1=right
    if lPar.isCongruent==1:
        posCue=lPar.posTarg
    else:
        posCue=1-lPar.posTarg
    
    fixX,fixL,fixR,cXLR,box,targ,mask1,mask2=createStim()
    frames.append(cXLR)
    box[posCue].fillColor=[1,1,1]
    frames.append(visual.BufferImageStim(win,stim=box+[fixX]))
    box[posCue].fillColor=[-1,-1,-1]
    frames.append(cXLR)
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,targ)))
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask1)))
    frames.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask2)))
    stamps=el.runFrames(win,frames,frameDurations,trialClock)
    ans=getResp()
    return(ans)

def runBlock(blk):
    blockStart(blk)
    if (blk==0) | (blk==2) | (blk==4):
        lPar.isCongruent=1                  #congruent
    else:
        lPar.isCongruent=0                  #incongruent

    lPar.dur=50
    numCor=0

    for trl in range(5):
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

def p1(): #click through
    messagep1=visual.TextStim(win,"Practice 1: \n\nClick your way through each step of the experiment.",height=30)
    messagep1.draw()
    win.flip()
    event.waitKeys()

    fixX,fixL,fixR,cXLR,box,targ,mask1,mask2=createStim()
    for trl in range(2):
        cXLR.draw()
        mes1=visual.TextStim(win,"This is the start screen. This will appear throughout the experiment",height=20,pos=(0,200),color=(1,1,1))
        mes2=visual.TextStim(win,"First, one of the boxes will flash white. \nThis is the cue. \n\nClick to see the cue",height=20,pos=(0,-200),color=(1,1,1))
        mes1.draw()
        mes2.draw()
        win.flip()
        event.waitKeys()
        cXLR.draw()
        box[trl].fillColor=[1,1,1]
        box[trl].draw()
        win.flip()
        core.wait(0.006)
        cXLR.draw()
        win.flip()
        core.wait(1.5)
        cXLR.draw()
        mes3=visual.TextStim(win,"Great! That was the cue. \n\nNext, a letter will flash in one of the boxes. \nFor this practice, it will be in the same box as the cue.",height=20,pos=(0,200),color=(1,1,1))
        mes4=visual.TextStim(win,"You're job is to report what letter you saw.\n\nClick to see the letter",height=20,pos=(0,-200),color=(1,1,1))
        mes3.draw()
        mes4.draw()
        win.flip()
        event.waitKeys()
        cXLR.draw()    
        targ.draw()
        win.flip()
        core.wait(0.012)
        cXLR.draw()
        win.flip()
        core.wait(0.5)
        cXLR.draw()
        mes5=visual.TextStim(win,"What letter did you see? \n(click answer on keyboard)",height=20,pos=(0,-200),color=(1,1,1))
        mes5.draw()
        win.flip()
        event.waitKeys()
        cXLR.draw()
        mes6=visual.TextStim(win,"Nice job! \nAfter the letter flashes, it will be covered by two symbols.",height=20,pos=(0,200),color=(1,1,1))
        mes7=visual.TextStim(win,"Here is what it will look like.\n\n(click to see letter and symbols)",height=20,pos=(0,-200),color=(1,1,1))
        mes6.draw()
        mes7.draw()
        win.flip()
        event.waitKeys()
        cXLR.draw()    
        targ.draw()
        win.flip()
        core.wait(0.01)
        cXLR.draw()
        mask1.draw()
        win.flip()
        core.wait(0.1)
        cXLR.draw()
        mask2.draw()
        win.flip()
        core.wait(0.1)
        cXLR.draw()
        win.flip()
        cXLR.draw()
        core.wait(1)
        win.flip()
        cXLR.draw()
        mes8=visual.TextStim(win,"That's what the experiement looks like. \nNot that much too it, right?",height=20,pos=(0,200),color=(1,1,1))
        mes9=visual.TextStim(win,"Let's run it through again \n(click to continue)",height=20,pos=(0,-200),color=(1,1,1))
        mes8.draw()
        mes9.draw()
        win.flip()
        event.waitKeys()

def p2(): #slow
    messagep2=visual.TextStim(win,"Practice 2: \n\nLet's run the experiment SLOWLY.",height=30)
    messagep2.draw()
    win.flip()
    event.waitKeys()

    for trial in range(8):
        Pframes=[]
        PframeDurations=[60,3,100,10,10,10]

        lPar.target = int(rng.integers(0,9,1))
        lPar.posTarg = int(rng.integers(0,2,1))  #0=left, 1=right
        if trial<=3:
            posCue=lPar.posTarg
        else:
            posCue=1-lPar.posTarg

        if trial==0:
            cong=visual.TextStim(win,"Same side",height=20)
            cong.draw()
            win.flip()
            core.wait(1)
        elif trial==4:
            incong=visual.TextStim(win,"Opposite side",height=20)
            incong.draw()
            win.flip()
            core.wait(1)
    
        fixX,fixL,fixR,cXLR,box,targ,mask1,mask2=createStim()
        Pframes.append(cXLR)
        box[posCue].fillColor=[1,1,1]
        Pframes.append(visual.BufferImageStim(win,stim=box+[fixX]))
        box[posCue].fillColor=[-1,-1,-1]
        Pframes.append(cXLR)
        Pframes.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,targ)))
        Pframes.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask1)))
        Pframes.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask2)))
        stamps=el.runFrames(win,Pframes,PframeDurations,trialClock)
        ans=getResp()

def p3(): #real thing
    messagep3=visual.TextStim(win,"Practice 3: \n\nLet's run the experiment \nAT SPEED.",height=30)
    messagep3.draw()
    win.flip()
    event.waitKeys()

    for trial in range(20):
        Pframes=[]
        PframeDurations=[60,1,lPar.dur,5,5,5]

        lPar.target = int(rng.integers(0,9,1))
        lPar.posTarg = int(rng.integers(0,2,1))  #0=left, 1=right
        if trial<=9:
            posCue=lPar.posTarg
        else:
            posCue=1-lPar.posTarg
    
        if trial==0:
            cong=visual.TextStim(win,"Same side",height=20)
            cong.draw()
            win.flip()
            core.wait(1)
        elif trial==10:
            incong=visual.TextStim(win,"Opposite side",height=20)
            incong.draw()
            win.flip()
            core.wait(1)

        fixX,fixL,fixR,cXLR,box,targ,mask1,mask2=createStim()
        Pframes.append(cXLR)
        box[posCue].fillColor=[1,1,1]
        Pframes.append(visual.BufferImageStim(win,stim=box+[fixX]))
        box[posCue].fillColor=[-1,-1,-1]
        Pframes.append(cXLR)
        Pframes.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,targ)))
        Pframes.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask1)))
        Pframes.append(visual.BufferImageStim(win,stim=(fixX,fixL,fixR,mask2)))
        stamps=el.runFrames(win,Pframes,PframeDurations,trialClock)
        ans=getResp()

def blockStart(blk):
    if (blk==0) | (blk==2) | (blk==4):
        cond = "Same side"
    else:
        cond = "Opposite side"
    message=visual.TextStim(win,f"Block {blk+1}  \n{cond} \n\nPress key to start",height=30)
    message.draw()
    win.flip()
    event.waitKeys()

def startExp():
    message=visual.TextStim(win,"Feeling ready? \n\nNow we will start the experiment blocks. \n\nPress a key to continue.",height=30)
    message.draw()
    win.flip()
    event.waitKeys()

def intro():
    messageIntro=visual.TextStim(win,"Welcome to the experiment! \n\nWe will start with some practice blocks.\n\nPress any key to begin practicing.",height=30)
    messageIntro.draw()
    win.flip()
    event.waitKeys()

#intro()
#p1()
#p2()
#p3()
startExp()
blocks=[0,1,2,3,4,5]
for i in range(int(len(blocks))): 
    blk=blocks[i]
    runBlock(blk)
win.close()
fptr.close
core.quit()

