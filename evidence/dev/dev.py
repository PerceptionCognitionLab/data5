from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random  
rng = random.default_rng()

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
correctSound1 = sound.Sound(500,secs = 0.25)
correctSound2 = sound.Sound(1000,secs = 0.25)

def playSound():
    correctSound1.play()
    core.wait(0.25)
    correctSound2.play()
    core.wait(0.25)

def displayDots(mu,sd):
    neg = rng.integers(0,2)
    if(neg == 0):
        correct = 'x'
    else:
        correct = 'm'
    coordinates = []
    for i in range(31):
        coordinates.append(np.round(np.random.normal(mu*(neg*2-1),sd)))
    for i in range(coordinates):
        circ=visual.Circle(win, pos=(coordinates[i],0), fillColor=[1, 1, 1], radius=5)
        circ.draw()
        win.flip()
        core.wait(.3)
        if(event.getKeys(['x'])):
            if(correct == 'x'):
                playSound()
            return correct,'x',i,coordinates
        if(event.getKeys(['m'])):
            if(correct == 'm'):
                playSound()
            return correct,'m',i,coordinates
    return correct,'no response',i,coordinates

def trial(numTrials,mu,sd):
    correctResponse = ()
    numDots = ()
    coordinates = np.empty()
    for i in range(numTrials+1):
        data = displayDots(mu,sd)
        correctResponse.append(data[0]==data[1])
        numDots.append(data[2])
        np.append(coordinates,np.array(coordinates[3]))
    return correctResponse,numDots,coordinates

print(trial(5,25,125))

win.close()
core.quit()