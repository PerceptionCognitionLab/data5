
from psychopy import core, visual, event, sound
import random
import decimal
import sys
import os
import numpy as np
from expLib51 import *

SCRIPT_DIR=os.environ.get('SCRIPT_DIR')
sys.path.append(SCRIPT_DIR)


win=visual.Window(units="pix",
                  size=(256,256), 
                  color=[0,0,0],
                  fullscr = True,
                  allowGUI=False)
fps=round(win.getActualFrameRate())
win.close()
if fps!=60:
    print()
    print("WARNING....  Frame Rate is not 60hz.")
    input("Enter to Continue, control-c to quit.  ") 


dbConf = data5
expName='ev1'
[pid,sid,fptr]=startExp(expName,dbConf,pool=1,lockBox=True)

# Create window and components
win = visual.Window(units="pix", size=(1024, 768), color="black", fullscr=True)
mouse = event.Mouse(visible=True)
timer = core.Clock()
seed = random.randrange(1e6)
print(pid,sid,"Jeff Rocks", sep=", ",file=fptr)

fptr.close()

hz=round(win.getActualFrameRate())
size=win.size
win.close()
stopExp(sid,hz,size[0],size[1],seed,dbConf)
core.quit()

	












