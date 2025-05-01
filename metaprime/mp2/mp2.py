# This is the modified experiment code with up/down arrows and left/right position change
import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import random
from psychopy import visual, core, event, prefs
import expLib51 as exlib
import numpy as np
import os

# region
refreshRate=165
exlib.setRefreshRate(refreshRate)
trialClock=core.Clock()
expName="mp1"
dbConf=exlib.data5
seed = random.randrange(1e6)
# [pid,sid,fname]=exlib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname] = [1,1,'Me.dat']
fptr = open(fname,'w')
# endregion

num_blocks = 1
n_trials_per_condition = 3
ISI_frames = [0, 4, 8, 12, 16, 28]
num_trials_per_block = 144
primeFrame = 2
maskFrame = 7
gap = 0.2
practice_num = 5

bg_color = np.array([1, 1, 1]) * 3 / 4
sti_color = np.array([-1, -1, -1]) * 3 / 4

win = visual.Window(units="pix", size=(1920, 1080), color=bg_color, fullscr=True)

welcome_text1 = visual.TextStim(win, text='Welcome to the experiment! Press spacebar to continue.', pos=(0, 0), color=sti_color)
welcome_text2 = visual.TextStim(win, text='The experiment contains two sessions. Each session has three blocks (~15 minutes).\nPress space bar to start the first session.', pos=(0, 0), color=sti_color)
instruction_text1 = visual.TextStim(win, text='You will see a flashing arrow. Identify the orientation (UP/DOWN).\n\n"x" for UP, "m" for DOWN.\n\nPress spacebar to continue.', pos=(0, 0), color=sti_color)
rest_text = visual.TextStim(win, text='Session 1 ends. Take a short break.\n\nPress spacebar to start session 2.', pos=(0, 0), color=sti_color)
instruction_text2 = visual.TextStim(win, text='You may notice a smaller arrow inside the big one. Identify its direction (UP/DOWN), ignoring the outer arrow.\n\n"x" for UP, "m" for DOWN.\n\nThis is harder. Do your best. Press spacebar to continue.', pos=(0, 0), color=sti_color)
goodbye_text = visual.TextStim(win, text='Experiment finished!\n\nPress spacebar to exit.', pos=(0, 0), color=sti_color)
start_practice_text = visual.TextStim(win, text='Practice trials begin. Feedback will be shown.\n\nPress space to start.', pos=(0, 0), color=sti_color)
end_practice_text = visual.TextStim(win, text='Practice finished.\n\nPress space to start the real experiment.', pos=(0, 0), color=sti_color)
fixation = visual.TextStim(win, text='+', pos=(0, 0), color=sti_color, bold=True, height=40)

prime_square = visual.ShapeStim(
    win=win, vertices=[(40,40),(40,-40),(-40,-40),(-40,40)],
    fillColor=sti_color, lineColor=sti_color, size=1)
prime_diamond = visual.ShapeStim(
    win=win, vertices=[(40,40),(40,-40),(-40,-40),(-40,40)],
    fillColor=sti_color, lineColor=sti_color, size=1, ori=45)

mask_outer_square = visual.ShapeStim(
    win=win, vertices=[(80, 80), (80, -80), (-80, -80), (-80, 80)],
    fillColor=sti_color , lineColor=sti_color, size=1, ori = 0)
mask_outer_diamond = visual.ShapeStim(
    win=win, vertices=[(80, 80), (80, -80), (-80, -80), (-80, 80)],
    fillColor=sti_color , lineColor=sti_color, size=1, ori = 45)
mask_inner_square = visual.ShapeStim(
    win=win, vertices=[(40*2**0.5,40*2**0.5),(40*2**0.5,-40*2**0.5),(-40*2**0.5,-40*2**0.5),(-40*2**0.5,40*2**0.5)],
    fillColor=bg_color, lineColor=bg_color, size=1)
mask_inner_diamond = visual.ShapeStim(
    win=win, vertices=[(40*2**0.5,40*2**0.5),(40*2**0.5,-40*2**0.5),(-40*2**0.5,-40*2**0.5),(-40*2**0.5,40*2**0.5)],
    fillColor=bg_color, lineColor=bg_color, size=1, ori = 45)

def run_trial(block_num, trial_num, prime_direction, mask_direction, ISI, position, provide_feedback=False, goal=None):
    true = mask_direction if goal == 'mask' else prime_direction
    prime = prime_square if prime_direction == 'square' else prime_diamond
    mask_outer = mask_outer_square if mask_direction == 'square' else mask_outer_diamond
    mask_inner = mask_inner_diamond if mask_direction == 'square' else mask_inner_square

    pos = (0, 200) if position == 'up' else (0, -200)
    mask_outer.pos = pos
    mask_inner.pos = pos
    prime.pos = pos
    mask = visual.BufferImageStim(win, stim=[mask_outer, mask_inner])
    prime = visual.BufferImageStim(win, stim=[prime, fixation])
    mask = visual.BufferImageStim(win, stim=[mask, fixation])
    wait = visual.BufferImageStim(win, stim=[fixation])

    pos = (0, 200) if position == 'up' else (0, -200)
    prime.pos = pos
    mask.pos = pos

    if ISI != 0:
        frames = [wait, prime, wait, mask]
        frameDurations = [120, primeFrame, ISI, maskFrame]
        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)
        critTime = exlib.actualFrameDurations(frameDurations, stamps)[2]
        critPass = (np.abs((ISI / refreshRate) - critTime) < .001)
        if not critPass:
            print(f'Critical pass fail at trial {trial_num} : crit={np.round(critTime, 4)} vs ideal={np.round(ISI / refreshRate, 4)}')
    else:
        frames = [wait, prime, mask]
        frameDurations = [120, primeFrame, maskFrame]
        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)

    trialClock.reset()
    fixation.draw()
    win.flip()
    keys = event.waitKeys(maxWait=5, timeStamped=trialClock, keyList=['x', 'm'])

    if keys:
        key, rt = keys[0]
        response = 'square' if key == 'x' else 'diamond'
        correctness = (response == true)
    else:
        response, rt, correctness = None, None, False

    if provide_feedback:
        feedback_text = 'Correct!' if correctness else 'Incorrect!'
        feedback = visual.TextStim(win, text=feedback_text, pos=(0, 0), color=sti_color)
        feedback.draw()
        win.flip()
        core.wait(1)
    else:
        win.flip()
        core.wait(0.2)

    output = [pid, sid, goal, (block_num - 1) * num_trials_per_block + trial_num, block_num, trial_num, prime_direction, mask_direction, prime_direction == mask_direction, round(ISI * 0.006, 3), position, response, round(rt, 3) if rt else rt, correctness]
    if not provide_feedback:
        print(output)
        print(*output, sep=',', file=fptr)

def run_practice_block(n_trials=practice_num, goal=None):
    start_practice_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    conditions = []
    for _ in range(n_trials):
        ISI = random.choice(ISI_frames)
        position = random.choice(['up', 'down'])
        prime_direction = random.choice(['square', 'diamond'])
        mask_direction = random.choice(['square', 'diamond'])
        conditions.append({'prime': prime_direction, 'mask': mask_direction, 'ISI': ISI, 'position': position})
    random.shuffle(conditions)
    for trial_num, trial in enumerate(conditions):
        if 'escape' in event.getKeys():
            return True
        run_trial(0, trial_num + 1, trial['prime'], trial['mask'], trial['ISI'], trial['position'], provide_feedback=True, goal=goal)
    end_practice_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])
    return False

def run_block(block_num, n_trials_per_condition, ISI_frames, goal=None):
    conditions = []
    trial_num = 0
    for ISI in ISI_frames:
        for position in ['up', 'down']:
            for prime in ['square', 'diamond']:
                for mask in ['square', 'diamond']:
                    conditions.append({'prime': prime, 'mask': mask, 'ISI': ISI, 'position': position})
    trial_list = conditions * n_trials_per_condition
    random.shuffle(trial_list)
    for trial in trial_list:
        if 'escape' in event.getKeys():
            return True
        trial_num += 1
        run_trial(block_num, trial_num, trial['prime'], trial['mask'], trial['ISI'], trial['position'], goal=goal)
    return False

def run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal=None):
    if run_practice_block(goal=goal):
        return
    for block_num in range(1, num_blocks + 1):
        if run_block(block_num, n_trials_per_condition, ISI_frames, goal=goal):
            break
        if block_num < num_blocks:
            break_text = visual.TextStim(win, text=f'Block {block_num} finished\nPress space to continue.', pos=(0, 0), color=sti_color)
            break_text.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

# The experiment skeleton
# region
# welcome1
welcome_text1.draw()
win.flip()
event.waitKeys(keyList=['space'])

# welcome2
welcome_text2.draw()
win.flip()
event.waitKeys(keyList=['space'])

# instruction1
mask_outer_square.pos = (0, -300)
mask_inner_diamond.pos = (0, -300)
mask = visual.BufferImageStim(win, stim=[mask_outer_square, mask_inner_diamond])
mask.draw()
instruction_text1.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Run the mask experiment
all_results = run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal = 'mask')

# rest
rest_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# instruction2
mask_outer_diamond.pos = (0, -300)
mask_inner_square.pos = (0, -300)
mask = visual.BufferImageStim(win, stim=[mask_outer_diamond, mask_inner_square])
prime_square.pos = (0,-300)
mask.draw()
prime_square.draw()
instruction_text2.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Run the prime experiment
all_results = run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal = 'prime')

# Show goodbye screen
goodbye_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Record settings and close the window
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
# exlib.stopExp(sid,hz,resX,resY,seed,dbConf)

win.close()
# Get everything in the store file and close the file
fptr.flush()
# endregion