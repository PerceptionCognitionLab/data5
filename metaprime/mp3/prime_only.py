import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import random
from psychopy import visual, core, event, prefs
import expLib51 as exlib
import numpy as np
import os
from psychopy import monitors

# Housekeeping
refreshRate=165
exlib.setRefreshRate(refreshRate)
trialClock=core.Clock()
expName="mp2_test"
dbConf=exlib.data5
seed = random.randrange(1e6)
# [pid,sid,fname]=exlib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname] = [1,1,'Me.dat']
fptr = open(fname,'w')
# endregion

# Define monitor
monitor = monitors.Monitor("MyMonitor")
monitor.setSizePix((1920, 1080))
monitor.setWidth(53.1)
monitor.setDistance(100)
monitor.saveMon()

# Experiment settings
num_blocks = 1
n_trials_per_condition = 3
# ISI_frames = [0, 4, 8, 12, 16, 20]
ISI_frames = [1]
num_trials_per_block = 12
primeFrame = 2
maskFrame = 7 
gapFrame = 120
gap = 0.2

# Stimulus settings
pos_text = (0,3.5)
ori_left = -45
ori_right = 45
prime_size = 3
mask_size = 4.5
blur_size = 7.2
text_height = 0.5
stimulus_contrast = 0.75
blur_contrast = 0.2
sf = 1.5
text_color = [-1,-1,-1]
bg_color = [0, 0, 0]
win_size = (1920, 1080)
center = (0,0)

# Define stimuli
win = visual.Window(units="deg", monitor = monitor, size=win_size, color= bg_color, fullscr=True)

fixation = visual.TextStim(win, text=' ', pos=center, color = text_color, bold = True, height = 0.7)
prime_left = visual.GratingStim(win=win, tex="sin", size=prime_size, sf=sf, ori=ori_left, contrast=stimulus_contrast, mask='gauss')
prime_right = visual.GratingStim(win=win, tex="sin", size=prime_size, sf=sf, ori=ori_right, contrast=stimulus_contrast, mask='gauss')
mask_left = visual.GratingStim(win=win, tex="sin", size=mask_size, sf=sf, ori=ori_left, contrast=stimulus_contrast, mask='circle')
mask_right = visual.GratingStim(win=win, tex="sin", size=mask_size, sf=sf, ori=ori_right, contrast=stimulus_contrast, mask='circle')
blur_region = visual.GratingStim(win=win, tex=None, size=blur_size, sf=0, mask="gauss", color=bg_color, contrast=blur_contrast)

# Define a function for a single trial 
def run_trial(block_num, trial_num, prime_direction, mask_direction, ISI, goal=None):
    if goal == 'mask':
        true = mask_direction
    else:
        true = prime_direction  

    prime = prime_left if prime_direction == 'left' else prime_right
    mask = mask_left if mask_direction == 'left' else mask_right

    prime.pos = center
    mask.pos = center
    blur_region.pos = center

    prime = visual.BufferImageStim(win, stim=[prime, fixation])
    mask = visual.BufferImageStim(win, stim=[mask, blur_region, fixation])
    wait = visual.BufferImageStim(win, stim=[fixation])

    if ISI != 0:
        frames = [wait, prime, wait, mask]
        frameDurations = [gapFrame, primeFrame, ISI, maskFrame]
        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)
        critTime = exlib.actualFrameDurations(frameDurations, stamps)[2]
        critPass = (np.absolute((ISI/refreshRate) - critTime) < .001)
        if not critPass:
            print('Critical pass fail at trial ' + str(trial_num) + ' : while critical time is ' + str(np.round(critTime, 4)) +
                  ', actual time is ' + str(np.round(ISI/refreshRate, 4)))
    else:
        frames = [wait, prime, mask]
        frameDurations = [gapFrame, primeFrame, maskFrame] 
        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)

    trialClock.reset()
    win.flip()
    keys = event.waitKeys(maxWait=5, timeStamped=trialClock, keyList=['x', 'm'])

    if keys:
        key, rt = keys[0]
        response = 'left' if key == 'x' else 'right'
        correctness = (response == true)
    else:
        response, rt, correctness = None, None, False


    feedback_text = 'Correct!' if correctness else 'Incorrect!'
    feedback = visual.TextStim(win, text=feedback_text, pos=center, color = [-1, -1, -1], height = 0.7)
    feedback.draw()
    win.flip()
    core.wait(1)


    output = [pid, sid, goal, (block_num - 1) * num_trials_per_block + trial_num, block_num, trial_num,
              prime_direction, mask_direction, prime_direction == mask_direction,
              np.round(ISI * 0.006, 3), response, np.round(rt, 3) if rt is not None else rt, correctness]

    print(output)
    print(*output, sep=',', file=fptr)

def run_block(block_num, n_trials_per_condition, ISI_frames, goal=None):
    conditions = []
    trial_num = 0
    for ISI in ISI_frames:
        conditions.append({'prime': 'left', 'mask': 'left', 'ISI': ISI})
        conditions.append({'prime': 'right', 'mask': 'right', 'ISI': ISI})
        conditions.append({'prime': 'left', 'mask': 'right', 'ISI': ISI})
        conditions.append({'prime': 'right', 'mask': 'left', 'ISI': ISI})

    trial_list = conditions * n_trials_per_condition
    random.shuffle(trial_list)

    for trial in trial_list:
        if 'escape' in event.getKeys():
            return True
        trial_num += 1
        run_trial(block_num=block_num, trial_num=trial_num,
                  prime_direction=trial['prime'], mask_direction=trial['mask'],
                  ISI=trial['ISI'], goal=goal)
    return False

def run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal=None):
    for block_num in range(1, num_blocks + 1):
        print(f"Running Block {block_num}...")
        quit_experiment = run_block(block_num, n_trials_per_condition, ISI_frames, goal=goal)
        if quit_experiment:
            print("Experiment quit by user.")
            break
        if block_num < num_blocks:
            break_text = visual.TextStim(win, text=f'Block {block_num} finished\nPress space to continue', pos=center, color=[-1, -1, -1])
            break_text.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

# Instruction text (only prime related)
welcome_text1 = visual.TextStim(win, text='Welcome to the experiment! Press space to continue.', height=text_height, pos=pos_text, color='black')
welcome_text2 = visual.TextStim(win, text='The experiment contains three blocks and lasts around 15 minutes.\n\nPress space to start.', height=text_height, pos=pos_text, color=text_color)

prime_text1 = visual.TextStim(win, text='Your task is to identify the orientation of the smaller grating.\n\nPress X for up-left, M for up-right.\n\nPress space to start the experiment', height=text_height, pos=pos_text, color=text_color)

goodbye_text = visual.TextStim(win, text='Experiment finished! Thank you!\n\nPress spacebar to exit.', height=text_height, pos=pos_text, color='black')

# Workflow
welcome_text1.draw()
win.flip()
event.waitKeys(keyList=['space'])

welcome_text2.draw()
win.flip()
event.waitKeys(keyList=['space'])

prime_text1.draw()
win.flip()
event.waitKeys(keyList=['space'])

run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal='prime')

goodbye_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

hz = round(win.getActualFrameRate())
[resX, resY] = win.size
#exlib.stopExp(sid,hz,resX,resY,seed,dbConf)
win.close()
fptr.flush()


# Read the data back
import pandas as pd
data = pd.read_csv(fname, header=None)
data.columns = [
    'pid', 'sid', 'goal', 'global_trial', 'block', 'trial_in_block',
    'prime_direction', 'mask_direction', 'congruency',
    'ISI', 'response', 'rt', 'correctness'
]
# Group by ISI and calculate mean correctness
isi_correctness = data.groupby('ISI')['correctness'].mean()
# Print the results
print("\n=== Average Correctness for each ISI ===")
print(isi_correctness)