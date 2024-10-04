
from psychopy import core, visual, event, sound
import random
import decimal
import sys
import numpy as np
import localLib

# Initialize experiment
expName = "dev.ev4"
runMode = False
[fptr, sub] = localLib.startExp(expName, runMode)

# Create window and components
win = visual.Window(units="pix", size=(1024, 768), color="black", fullscr=True)
mouse = event.Mouse(visible=True)
timer = core.Clock()
seed = random.randrange(1e6)
rng = random.Random(seed)
dot_size = 5

max_trials = 30
frame_dur = 30

## Sounds
correct1=sound.Sound(500,secs=.1)
correct2=sound.Sound(1000,secs=.2)
error=sound.Sound(250,secs=.5)

# Create stimuli
fix = visual.TextStim(win, text="Ready?", height=30, color='white')
dot = visual.Circle(win, radius=5, units="pix", fillColor=[1, 1, 1])

# Functions
def show_instructions():
	start_text = "In this experiment you can only press either X or M. Press Any Key to Start"
	start_stim = visual.TextStim(
		win, 
		text=start_text, 
		height=20, 
		color='white')
	start_stim.draw()
	win.flip()
	event.waitKeys()

def draw_dividers():
	divider_low = visual.Line(
		win=win, 
		start=(0, -584), 
		end=(0, -400), 
		lineColor=[1, 0, 0])
	divider_high = visual.Line(
		win=win, 
		start=(0, 400), 
		end=(0, 584), 
		lineColor=[1, 0, 0])
	divider_low.draw()
	divider_high.draw()



def do_trial(mean):
	event.clearEvents()
	current_frame = 0
	
	x0 = np.rint(np.random.normal(mean, 100, size=max_trials))
	x = np.repeat(x0, frame_dur)
	resp = []
	fix.draw()
	win.flip()
	core.wait(1)
	dot.pos=[0,0]
	draw_dividers()
	dot.draw()
	win.flip()
	core.wait(0.4)
	correct_resp = 'm' if mean > 0 else 'x'
	while current_frame < (max_trials * frame_dur) and not resp:
		draw_dividers()
		dot.pos = [x[current_frame], 0]
		dot.draw()
		win.flip()

		current_frame = current_frame + 1
		resp = event.getKeys(keyList=['x', 'm', 'escape'])

		if 'escape' in resp:
			
			return None, 'Abort', None
		elif resp:
			correct = resp[0] == correct_resp
			if correct:
				correct2.play()
			else:
				error.play()
			break
		

	return current_frame, resp[0] if resp else None, x0, correct

# Main experiment
show_instructions()
#+50 on right -50 on left
conditions = [-50,-50,-50,-50,-50,50,50,50,50,50]
random.shuffle(conditions)

for condition in conditions:
	[rt, resp, x, correct] = do_trial(condition)

	if resp == 'Abort':
		print("Experiment Aborted")
		break

	print(sub, rt, resp, *x, correct, sep=", ", file=fptr)
	fptr.flush()

# Close files and windows
fptr.close()
win.close()
core.quit()




