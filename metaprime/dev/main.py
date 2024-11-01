import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import random
from psychopy import visual, core, event, prefs
import expLib51 as exlib
import numpy as np
import os
# Housekeeping
# region
refreshRate=165
exlib.setRefreshRate(refreshRate)
trialClock=core.Clock()
expName="devmp1"
dbConf=exlib.beta
seed = random.randrange(1e6)
# [pid,sid,fname]=exlib.startExp(expName,dbConf,pool=1,lockBox=False,refreshRate=refreshRate)
fname = 'test.dat'
fptr = open(fname,'w')
# endregion


# Set up the window
win = visual.Window(units="pix", size=(1920, 1080), color='black', fullscr=True)

# Experiment settings
# region
num_blocks = 3
n_trials_per_condition = 5
ISI_frames = [2]

# endregion

# Define stimuli: primes, masks, text
#region
# Text stimuli
welcome_text = visual.TextStim(win, text='Welcome to the experiment\nPress space to continue', pos=(0, 0), color="white")
goodbye_text = visual.TextStim(win, text='Experiment finished!\nThank you for your participation\nPress space to exit', pos=(0, 0), color="white")
wait_text = visual.TextStim(win, text='Choose the direction', pos=(0, -300), color="red")
choose_text = visual.TextStim(win, text='Choose the direction', pos=(0, -300), color="green")

# Fixation and blank
fixation = visual.TextStim(win, text='+', pos=(0, 0), color="white", bold = True, height = 80)

prime_left = visual.ShapeStim(
    win=win, vertices=[(-100,0),(-75,25),(100,25),(75,0),(100,-25),(-75,-25)],
    fillColor="white", lineColor="white", size=1)
prime_right = visual.ShapeStim(
    win=win, vertices=[(-75,0),(-100,25),(75,25),(100,0),(75,-25),(-100,-25)],
    fillColor="white", lineColor="white", size=1)
mask_left = visual.ShapeStim(
    win=win, vertices=[(-165, 0), (-120, 45), (120, 45), (120, -45), (-120, -45)],
    fillColor="white", lineColor="white", size=1)
mask_right = visual.ShapeStim(
    win=win, vertices=[(-120, 45), (120, 45), (165,0), (120, -45), (-120, -45)],
    fillColor="white", lineColor="white", size=1)
mask_inner = visual.ShapeStim(
    win=win, vertices=[(-105,30),(105,30),(90,15),(105,0),(90,-15),(105,-30),(-105,-30),(-90,-15),(-105,0),(-90,15)],
    fillColor="black", lineColor="black", size=1)
#endregion

# Define a function for a single trial
def run_trial(trial_num, prime_direction, mask_direction, ISI, position): 
    # Set the orientation of the prime used in this trial
    prime = prime_left if prime_direction == 'left' else prime_right
    mask_outer = mask_left if mask_direction == 'left' else mask_right
    
    # Set position for both prime and mask either at top or bottom of the fixation points
    pos = (0, 130) if position == 'top' else (0, -130)
    prime.pos = pos
    mask_outer.pos = pos
    mask_inner.pos = pos

    # Include fixation and wait text point to the prime
    prime = visual.BufferImageStim(win,stim=[prime, fixation, wait_text])

    # Combine the two components of the mask and fixation and wait text together
    mask = visual.BufferImageStim(win,stim=[mask_outer, mask_inner, fixation, wait_text])
    
    # Wait screen
    wait = visual.BufferImageStim(win,stim=[fixation, wait_text])

    # Run frames
    if ISI != 0:
        frames = [wait, prime, wait, mask]
        frameDurations = [120, 7, ISI, 12]
        stamps=exlib.runFrames(win,frames,frameDurations,trialClock)
        critTime=exlib.actualFrameDurations(frameDurations,stamps)[2]
        critPass=(np.absolute((ISI/refreshRate)-critTime)<.001)
        if not critPass:
            print('Critical pass fail at trial ' +str(trial_num)+' : while critical time is '+str(np.round(critTime,4))+
                ', actual time is '+str(np.round(ISI/refreshRate,4)))
    else:
        frames = [wait, prime, mask]
        frameDurations = [120, 7, 12] 
        stamps=exlib.runFrames(win,frames,frameDurations,trialClock)

    # Record the reaction time and wait for response for at most 1.5s
    trialClock.reset()
    fixation.draw()
    choose_text.draw()
    win.flip()
    keys = event.waitKeys(maxWait=1.5, timeStamped=trialClock, keyList=['x','m'])
    # Check if the response was correct
    if keys:
        key, rt = keys[0]
        if key == 'x':
            response = 'left'
        else:
            response = 'right'
        correctness = (response == mask_direction)
        # correct = (key == prime_direction)
    else:
        response, rt, correctness = None, None, False  # No response is considered incorrect

    # Return trial result
    # Prime_direction, mask_direction, congruency，ISI_duration, position, response, rt, correct
    output = [
        prime_direction, 
        mask_direction, 
        prime_direction == mask_direction,
        np.round(ISI * 0.006,3), 
        position, 
        response, 
        np.round(rt,3) if rt != None else rt, 
        correctness]
    print(output)
    print(*output, sep=',', file=fptr)

# Define a function to run a block of trials
def run_block(n_trials_per_condition, ISI_frames):
    # Generate trial conditions
    conditions = []
    # Count on trial number
    trial_num = 0
    #Collect all conditions and shuffle
    for ISI in ISI_frames:
        for position in ['top', 'bottom']:
            conditions.append({'prime': 'left', 'mask': 'left', 'ISI': ISI, 'position': position})
            conditions.append({'prime': 'right', 'mask': 'right', 'ISI': ISI, 'position': position})
            conditions.append({'prime': 'left', 'mask': 'right', 'ISI': ISI, 'position': position})
            conditions.append({'prime': 'right', 'mask': 'left', 'ISI': ISI, 'position': position})

    # Shuffle and repeat trials for each condition
    trial_list = conditions * n_trials_per_condition
    random.shuffle(trial_list)

    # Run each trial in the block
    for trial in trial_list:
        # Check for escape key to quit
        if 'escape' in event.getKeys():
            return True  # Return results and signal to quit
        trial_num += 1
        # Run the trial and collect results
        run_trial(
            trial_num = trial_num,
            prime_direction=trial['prime'],
            mask_direction=trial['mask'],
            ISI=trial['ISI'],
            position=trial['position']
        )

    return False  # Return results and signal to continue

# Define a function to run the full experiment with multiple blocks
def run_experiment(num_blocks, n_trials_per_condition, ISI_frames):
    all_results = []

    for block_num in range(num_blocks):
        print(f"Running Block {block_num + 1}...")

        # Run a block of trials
        quit_experiment = run_block(n_trials_per_condition, ISI_frames)
        if quit_experiment:
            print("Experiment quit by user.")
            break  # Stop experiment if quit signal received

        # Pause between blocks (except last one)
        if block_num < num_blocks - 1:
            
            break_text = visual.TextStim(win, text=f'Block {block_num + 1} finished\nPress space to continue to the next block', pos=(0, 0), color="black")
            break_text.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

    return all_results

# The experiment skeleton
# region
welcome_text.draw()
win.flip()
event.waitKeys(keyList=['space'])
# Run the experiment
all_results = run_experiment(num_blocks, n_trials_per_condition, ISI_frames)
# Show goodbye screen
goodbye_text.draw()
win.flip()
event.waitKeys(keyList=['space'])
# Record settings and close the window
'''
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
exlib.stopExp(sid,hz,resX,resY,seed,dbConf)
'''
win.close()
# Get everything in the store file and close the file
fptr.flush()
# endregion


