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
expName = "pm1"
dbConf = elib.data5
[pid, sid, fname] = elib.startExp(expName, dbConf, pool=2, lockBox=False, refreshRate=refreshRate)
fptr = open(fname, "w")

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
mouse = event.Mouse(visible=False, newPos=[0, 0], win=win)  # mouse centered at zero
trialClock = core.Clock()
seed = random.randrange(1e6)
random.seed(seed)

fix = visual.TextStim(win, "+")  # fixation cross
blank = visual.TextStim(win, "")  # blank window
int_trial = 0
mask_trial = 20

gPar0 = {
    'spacing': 48,
    'sizeIndicator': [0, 1, 1, 1, 0]
}

def integrationTrial(soa, gPar, prac=False):
    [x, y] = [gPar['x'], gPar['y']]
    target = random.choice(gPar['validTarget'])
    [aDots, bDots] = support.intDotIndex(gPar, target)
    dots = [visual.Circle(win, pos=(x[i], y[i]), fillColor=[0, -1, -1], radius=2.5) for i in range(gPar['N'])]
    allRed = visual.BufferImageStim(win, stim=dots)
    adots = [visual.Circle(win, pos=(x[aDots[i]], y[aDots[i]]), fillColor=[1, 1, 1], radius=5) for i in range(len(aDots))]
    alldots = [visual.Circle(win, pos=(x[aDots[i]], y[aDots[i]]), fillColor=[1, 1, 1], radius=5) for i in range(len(aDots))]
    a = visual.BufferImageStim(win, stim=adots)
    bdots = [visual.Circle(win, pos=(x[bDots[i]], y[bDots[i]]), fillColor=[1, 1, 1], radius=5) for i in range(len(bDots))]
    alldots.extend([visual.Circle(win, pos=(x[bDots[i]], y[bDots[i]]), fillColor=[1, 1, 1], radius=5) for i in range(len(bDots))])
    b = visual.BufferImageStim(win, stim=bdots)
    frame = [fix, blank, a, blank, b, blank, allRed]
    frameDurations = [120, 60, 5, soa, 5, 60, 1]
    if prac:
        all = visual.BufferImageStim(win, stim=alldots)
        frame = [fix, blank, all, blank, blank, blank, allRed]
        frameDurations = [120, 60, 120, 1, 1, 60, 1]
    stamps = elib.runFrames(win, frame, frameDurations, trialClock)
    critTime = elib.actualFrameDurations(frameDurations, stamps)[3]
    critPass = (np.absolute(soa / refreshRate - critTime) < .001)
    resp = support.mouseResponse(mouse, win, gPar, frame[6])
    correct = target == resp
    support.feedback(correct)
    return [target, resp, correct, np.round(critTime, 4), critPass]

def maskingTrial(soa, gPar):
    [x, y] = [gPar['x'], gPar['y']]
    target = random.choice(gPar['validTarget'])
    maskDots = []
    redDots = []
    targetDots = [visual.Circle(win, pos=(x[target], y[target]), fillColor=[1, 1, 1], radius=5)]
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
    critPass = (np.absolute(soa / refreshRate - critTime) < .001)
    resp = support.mouseResponse(mouse, win, gPar, frame[6])
    correct = target == resp
    support.feedback(correct)
    return [target, resp, correct, np.round(critTime, 4), critPass]

def maskingTrialpractice(soa, gPar):
    [x, y] = [gPar['x'], gPar['y']]
    target = random.choice(gPar['validTarget'])
    maskDots = []
    redDots = []
    targetDots = [visual.Circle(win, pos=(x[target], y[target]), fillColor=[1, 1, 1], radius=5)]
    soaarray = []
    correctarray = []
    correctPrevious = 0
    inc = -1
    
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
    critPass = (np.absolute(soa / refreshRate - critTime) < .001)
    resp = support.mouseResponse(mouse, win, gPar, frame[6])
    correct = target == resp 
    correctarray.append(correct)
    soa, correctPrevious = support.stairCase(soa, correct, correctPrevious, inc)
    soaarray.append(soa)
    support.feedback(correct)

    
    if len(correctarray) >= 12:
        correctarray_np = np.array(correctarray)
        soaarray_np = np.array(soaarray)
        soa = np.mean(soaarray_np[-12:][correctarray_np[-12:] == 0])
    
    return [soa, soaarray, correctarray, target, resp, correct, np.round(critTime, 4), critPass]

def block(blk, task, trials, soa, gPar, inc=-1):
    correctPrevious = 0 
    for t in range(trials):
        input = [pid, sid, blk, task, t, soa]
        if (task == 0):
            result = integrationTrial(soa, gPar)
        elif (task == 1):
            result = maskingTrial(soa, gPar)
        output = input + result
        print(*output, sep=", ", file=fptr)
        soa, correctPrevious = support.stairCase(soa, result[2], correctPrevious, inc)
    return soa

#########

gPar = support.initGlobals(gPar0)  # adds x, y, validTarget, N to structure

soa = 15
inc = [1, -3, 1, -1, 1, -1]
taskBlk = [1, 1, 1, 1]
n = [5, 5, 5, 5]
numBlock = len(taskBlk)

support.instruct(win, mouse, "Welcome")
support.instruct(win, mouse, "Find The Flashed Dot")

for r in range(mask_trial):
    soa, soaarray, correctarray, target, resp, correct, critTime, critPass = maskingTrialpractice(soa, gPar)
soa = np.mean(np.array(soaarray)[np.array(correctarray) == 0])
support.instruct(win, mouse, "Great. Please Wait.")
print(soaarray)
print(correctarray)
print(soa)

for b in range(numBlock):
    tsk = taskBlk[b]
    txt = ["Find The Missing Dot\n\n (Right Mouse Button To Continue)",
           "Find The Flashed Dot\n\n (Right Mouse Button To Continue)"]
    support.instruct(win, mouse, txt[tsk])
    soa = block(b, tsk, n[b], soa, gPar, inc[b])
    print(soa)
    support.instruct(win, mouse, "Take A Break\n\n(Right Mouse Button When Done)")

# End of Experiment
fptr.flush()
support.instruct(win, mouse, "You Are Done!\n\n Thank You \n Please See Experimenter", advance="")
event.waitKeys(keyList=abortKey)
hz = round(win.getActualFrameRate())
resX, resY = win.size

win.close()
elib.stopExp(sid, hz, resX, resY, seed, dbConf)
os.system('cat *.dat >all.dat')
core.quit()
