# Imports
from psychopy import core, visual, event
import random
import numpy as np  
import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as elib
import support

# Housekeeping
abortKey = ['9']
refreshRate = 165
elib.setRefreshRate(refreshRate)
pid = 1
sid = 1

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
mouse = event.Mouse(visible=False, newPos=[0, 0], win=win)  # mouse centered at zero
trialClock = core.Clock()
seed = random.randrange(1e6)
random.seed(seed)

fix = visual.TextStim(win, "+")  # fixation cross
blank = visual.TextStim(win, "")  # blank window

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
    soapertrial=[]
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
    critPass = (np.absolute(soa / refreshRate - critTime) < .001)
    resp = support.mouseResponse(mouse, win, gPar, frame[6])
    correct = target == resp
    support.feedback(correct)
    soapertrial.append(soa)
    print(soapertrial)
    return [target, resp, correct, np.round(critTime, 4), critPass]

def block(blk, task, trials, soa, gPar, inc=1, first_block=True):
    correctPrevious = 0 
    soa_list = []
    for t in range(trials):
        input = [pid, sid, blk, task, t, soa]
        result = maskingTrial(soa, gPar)
        output = input + result
        if first_block:
            [soa, correctPrevious] = support.stairCase(soa, result[2], correctPrevious, inc)
            soa_list.append(soa)
        else:
            soa = random.randint(soa - 3, soa + 3)  
    return np.mean(soa_list, dtype=int) if soa_list else soa


#########

gPar = support.initGlobals(gPar0)  

soa = [15, 15]  
inc = [-1, -1, -1, -1, -1, -1]
taskBlk = [1, 1, 1, 1, 1, 1]
n = [5, 1, 1, 1, 1, 1]
numBlock = len(taskBlk)

support.instruct(win, mouse, "Welcome")
support.instruct(win, mouse, "Find The Missing Dot")
for b in range(numBlock):
    tsk = taskBlk[b]
    if b == 0:  # For the first block
        soa[tsk] = block(b, tsk, n[b], soa[tsk], gPar, inc[b], first_block=True)
    else:  # For subsequent blocks
        soa[tsk] = block(b, tsk, n[b], soa[tsk], gPar, inc[b], first_block=False)
    support.instruct(win, mouse, "Take A Break\n\n(Right Mouse Button When Done)")
    print(soa)

support.instruct(win, mouse, "You Are Done!\n\n Thank You \n Please See Experimenter", advance="")
a = event.waitKeys(keyList=abortKey)
hz = round(win.getActualFrameRate())
[resX, resY] = win.size

win.close()

core.quit()
