from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random  
rng = random.default_rng()

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)

val = rng.integers(0,2)
coordinates = []
for i in range(31):
    xVal = np.round(np.random.normal(25*(val*2-1),125))
    circ=visual.Circle(win, pos=(xVal,0), fillColor=[1, 1, 1], radius=5)
    circ.draw()
    win.flip()
    core.wait(.3)
    coordinates.append(xVal)
    if(event.getKeys(['x'])):
        print("Response: X")
        break
    if(event.getKeys(['m'])):
        print("Response: M")
        break

print("Number of shots: ",i)
print(coordinates)
win.close()
core.quit()