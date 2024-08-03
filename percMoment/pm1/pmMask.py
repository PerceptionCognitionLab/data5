# Imports
from psychopy import core, visual, sound, event, clock
import math 
import random
import decimal
import sys
import numpy as np  
import os
import time   
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as elib
import support

# Housekeeping
abortKey = ['9']
refreshRate = 165
elib.setRefreshRate(refreshRate)

sid = 1
pid = 1


# expName = "pm2"
# dbConf = elib.data5
# [pid, sid, fname] = elib.startExp(expName, dbConf, pool=2, lockBox=False, refreshRate=refreshRate)
# fptr = open(fname, "w")

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
mouse = event.Mouse(visible=False, newPos=[0, 0], win=win)  # Mouse centered at zero
trialClock = core.Clock()
seed = random.randrange(1e6)
random.seed(seed)

fix = visual.TextStim(win, "+")  # Fixation cross
blank = visual.TextStim(win, "")  # Blank window

gPar0 = {
    'spacing': 48,
    'sizeIndicator': [0, 1, 1, 1, 0]
}

def maskingTrial(soa, gPar):
    [x, y] = [gPar['x'], gPar['y']]
    target = random.choice(gPar['validTarget'])
    maskDots = []
    redDots = []
    targetDots = []
    targetDots.append(visual.Circle(win, pos=(x[target], y[target]), fillColor=[1, 1, 1], radius=5))
    for i in range(gPar['N']):
        if i != target:
            targetDots.append(visual.Circle(win, pos=(x[i], y[i]), fillColor=[0, -1, -1], radius=2.5))
        redDots.append(visual.Circle(win, pos=(x[i], y[i]), fillColor=[0, -1, -1], radius=2.5))
        maskDots.append(visual.Circle(win, pos=(x[i], y[i]), fillColor=[1, 1, 1], radius=5))
    allRed = visual.BufferImageStim(win, stim=redDots)
    mask = visual.BufferImageStim(win, stim=maskDots)
    targ = visual.BufferImageStim(win, stim=targetDots)
    frame = [fix, allRed, targ, allRed, mask, allRed, allRed]
    frameDurations = [120, 60, 1, soa, 20, 60, 1]
    stamps = elib.runFrames(win, frame, frameDurations, trialClock)
    critTime = elib.actualFrameDurations(frameDurations, stamps)[3]
    critPass = (np.absolute(soa/refreshRate - critTime) < .001)
    resp = support.mouseResponse(mouse, win, gPar, frame[6])
    correct = target == resp
    support.feedback(correct)
    return [target, resp, correct, np.round(critTime, 4), critPass]

def block(blk, task, trials, soa, gPar, inc=1):
    correctPrevious = 0 
    soaarray = [] 
    soathreshold = None  
    for t in range(trials):
        input = [pid, sid, blk, task, t, soa]
        if task == 0:
            result = maskingTrial(soa, gPar)
            [soa, correctPrevious] = support.stairCase(soa, result[2], correctPrevious, inc)
            soaarray.append(soa)

        elif task == 1:
            result = maskingTrial(soa, gPar)
            soa = random.randint(max(4, soa-3), soa+3)
     

        output = input + result
        #print(*output, sep=", ", file=fptr)  # Assuming fptr is defined globally

    if task == 0 and soaarray:  
        soathreshold = np.mean(np.array(soaarray))
    return soa, soathreshold


#########

gPar = support.initGlobals(gPar0)  # Adds x, y, validTarget, N to structure

soa = [15, soathreshold]
inc = [-1, -1, -1, -1, -1]
taskBlk = [0, 1, 1, 1, 1]
n = [1, 1, 1, 1, 1]
numBlock = len(taskBlk)

for b in range(numBlock):
    tsk = taskBlk[b]
    txt = ["Find The Flashed Dot\n\n (Right Mouse Button To Continue)",
           "Find The Flashed Dot\n\n (Right Mouse Button To Continue)"]
    support.instruct(win, mouse, txt[tsk])
    soa[tsk], soathreshold = block(b, tsk, n[b], soa[tsk], gPar, inc[b])
    support.instruct(win, mouse, "Take A Break\n\n(Right Mouse Button When Done)")

support.instruct(win, mouse, "You Are Done!\n\n Thank You \n Please See Experimenter", advance="")
a = event.waitKeys(keyList=abortKey)
hz = round(win.getActualFrameRate())
[resX, resY] = win.size

win.close()

# elib.stopExp(sid, hz, resX, resY, seed, dbConf)
# os.system('cat *.dat > all.dat')
core.quit()

