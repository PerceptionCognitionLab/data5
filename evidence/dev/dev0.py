from psychopy import core, visual, sound, event, clock
import numpy as np  

win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)

circ=visual.Circle(win, pos=(0,0), fillColor=[1, 1, 1], radius=5)
circ.draw()
win.flip()
event.waitKeys()

win.close()
core.quit()