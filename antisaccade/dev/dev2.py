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
    frameDurations=[60,1,lPar.dur,5,5,5,1]

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
    frames.append(visual.TextStim(
        win = win,
        text = "Enter the letter you saw",
        pos = (0,0),
        color = [0,1,0]
    ),)
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


#############
# training
#############

def fixiateFrame(frame):
    frame[-1].draw()
    win.flip() 

def trainFR():
    fixX,fixL,fixR,cXLR,box,targ,mask1,mask2=createStim()

    # Init
    frame=[]
    frameTimes=[1]
    txt1s1= visual.TextStim(win,"Practice 1:\nClick through the experiment.\n\nPress a key to continue",height=30)
    frame.append(txt1s1)
    
    el.runFrames(win,frame,frameTimes,trialClock)
    fixiateFrame(frame)
    getResp()

    # inst 2
    frame = []
    frameTimes=[1]
    txt1s1= visual.TextStim(win,"This is the start screen. This will appear throughout the experiment",pos=(0,200),height=20)
    txt1s2= visual.TextStim(win,"First, one of the boxes will flash white. \nThis is the cue. \n\nClick to see the cue", pos=(0,-200),height=20)
    frame.append(visual.BufferImageStim(win,stim=[txt1s1,txt1s2,fixL,fixR,fixX]))
    
    el.runFrames(win,frame,frameTimes,trialClock)
    fixiateFrame(frame)
    getResp()

    #cue
    frame = []
    frameTimes=[2,150]
    box[0].fillColor = [1, 1, 1]
    cue = visual.BufferImageStim(win, stim=box + [fixX])
    box[0].fillColor = [-1, -1, -1]
    frame.append(cue)
    frame.append(visual.BufferImageStim(win,stim=[fixX,fixL,fixR]))    
    
    el.runFrames(win, frame, frameTimes, trialClock)

    #inst 3
    frame = []
    frameTimes=[1]
    txt1s3 = visual.TextStim(win, "Looks good! That was the cue. \n\nNext, a letter from the middle row on the keyboard will flash in one of the boxes. \nFor this practice, it will be in the same box as the cue.", pos=(0, 200), height=20)
    txt1s4 = visual.TextStim(win, "Press a key to continue", pos=(0, -200), height=20)
    frame.append(visual.BufferImageStim(win, stim=[txt1s3, txt1s4, fixL, fixR, fixX]))
    
    el.runFrames(win,frame,frameTimes,trialClock)
    fixiateFrame(frame)
    getResp()

    #target
    stim='incorrect'
    while stim=='incorrect':
        frame = []
        frameTimes=[5,150,1]
        frame.append(targ)
        frame.append(visual.BufferImageStim(win,stim=[fixX,fixL,fixR]))
        test=visual.TextStim(win,"What letter did you see?",height=20,pos=(0,-200))
        frame.append(visual.BufferImageStim(win,stim=[test,fixX,fixL,fixR]))    
        [resp,rt]=getResp()

        el.runFrames(win, frame, frameTimes, trialClock)
        fixiateFrame(frame)
    
        if resp=='a':
            stim='correct'
            txt1s5 = visual.TextStim(win, "Nice job!\nClick to continue.", pos=(0,200), height=20)
        else:
            txt1s5 = visual.TextStim(win, "Not quite, let's try again.\nClick to see it again.", pos=(0,200), height=20)
        
        frame2 = []
        frameTimes2=[1]
        frame2.append(visual.BufferImageStim(win,stim=[txt1s5,fixX,fixL,fixR]))
        el.runFrames(win, frame2, frameTimes2, trialClock)
        fixiateFrame(frame2)



        


 




















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
trainFR()
startExp()
#blocks=[0,1,2,3,4,5]
#for i in range(int(len(blocks))): 
    #blk=blocks[i]
    #runBlock(blk)
win.close()
fptr.close
core.quit()

