import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import random
from psychopy import visual, core, event, prefs
import expLib51 as exlib
import numpy as np
import os
from psychopy import visual, core, monitors

# region
refreshRate=165
exlib.setRefreshRate(refreshRate)
trialClock=core.Clock()
expName="mp2_test"
dbConf=exlib.data5
seed = random.randrange(1e6)
[pid,sid,fname]=exlib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
# [pid,sid,fname] = [1,1,'Me.dat']
fptr = open(fname,'w')
# endregion

#define monitor
monitor = monitors.Monitor("MyMonitor")
monitor.setSizePix((1920, 1080))
monitor.setWidth(53.1)
monitor.setDistance(100)
monitor.saveMon()

# Experiment settings
# region
num_blocks = 3
n_trials_per_condition = 3
ISI_frames = [0, 4, 8, 12, 16, 20]
# ISI_frames = [0, 2, 4, 6, 8, 10, 12] # Vorberg's
num_trials_per_block = 144
primeFrame = 2
maskFrame = 7   # to find dissocniation
# maskFrame = 20
gap = 0.2
practice_num = 20
# endregion

# Define stimuli: primes, masks, text
#region

# Set up the window
win = visual.Window(units="deg", monitor = monitor, size=(1920, 1080), color= (0, 0, 0), fullscr=True)

# Text stimuli
welcome_text1 = visual.TextStim(win, text='Welcome to the experiment! Press space to continue.', height = 0.7, pos = (0,2.4), color = 'black')
welcome_text2 = visual.TextStim(win, text='The experiment contains two sessions. Each session has three blocks and lasts around 15 minutes.\n\nPress space to start the first session.', height = 0.7, pos = (0,2.4), color = [-1, -1, -1])
instruction_text1 = visual.TextStim(win, text='In this session, the grating shown below will flash on the screen. Your task is to identify the orientation of the grating as soon as you see it.\n\nIf you think the grating is oriented up-to-the-left, press X. If it is orientated up-to-the-right, press M. Below is an sample grating orientated to up-to-the-left.\n\nYou may see something flash at the center of the grating, please ignore it.\n\nPress space to continue', height = 0.5, pos = (0,2.4), color = 'black')
rest_text=  visual.TextStim(win, text='Session 1 ends! You may take a break before starting session 2.\n\nPress space to continue.', height = 0.7, pos = (0,2.4), color = [-1, -1, -1])
instruction_text2 = visual.TextStim(win, text= 'You may or may not have notice that there is a smaller grating appears at the center of the bigger ring (shown as below). In this session, your task is to identify the orientation of the smaller grating while neglecting the outer grating.\n\nIf you think the grating is oriented up-to-the-left, press X. If it is orientated up-to-the-right, press M.\n\nThis session is more difficult, please pay close attention. Press space to continue', height = 0.5 , pos = (0,3.5), color = 'black')
goodbye_text = visual.TextStim(win, text='Experiment finished! Thank you for participating!\n\nPress spacebar to exit', height = 0.7, pos=(0, 2.4), color = 'black')
start_practice_text = visual.TextStim(win, text='We will begin with some practice trials. We will provide feedback on your response. Note that in the real experiment there will be no feedback.\n\nPress space to start the practice trials.', height = 0.7, pos=(0, 2.4), color = 'black')
end_practice_text = visual.TextStim(win, text='Practice finished.\n\nPress space to start the real experiment.', height = 0.7, pos=(0, 2.4), color = 'black')

fixation = visual.TextStim(win, text='+', pos=(0, 0), color = 'black', bold = True, height = 0.7)
prime_left = visual.GratingStim(
    win=win,
    tex = "sin", 
    size = 3,  
    sf = 0.75,    
    ori = -45,  
    contrast = 0.75,
    mask = 'gauss'
)

prime_right = visual.GratingStim(
    win=win,
    tex = "sin", 
    size = 3, 
    sf = 0.75,    
    ori = 45,  
    contrast = 0.75,
    mask = 'gauss'
)

mask_left= visual.GratingStim(
    win = win,
    tex = "sin",
    size = 4.5, 
    sf = 0.75, 
    ori = -45,  
    contrast = 0.75,
    mask = 'circle',
)

mask_right = visual.GratingStim(
    win = win,
    tex = "sin",
    size = 4.5, 
    sf = 0.75, 
    ori = 45,  
    contrast = 0.75,
    mask = 'circle',
)
blur_region = visual.GratingStim(
    win = win,
    tex = None,  
    size= 7.2,  
    sf = 0,   
    mask = "gauss",  
    color = [0, 0, 0], 
    contrast = 0.2,  
)

# Define a function for a single trial 
def run_trial(block_num, trial_num, prime_direction, mask_direction, ISI, position, provide_feedback=False, goal = None): 
    # Set goal of the trial
    if goal == 'mask':
        true = mask_direction
    else:
        true = prime_direction  
    # Set the orientation of the prime used in this trial
    prime = prime_left if prime_direction == 'left' else prime_right
    mask = mask_left if mask_direction == 'left' else mask_right
    
    # Set position for both prime and mask either at top or bottom of the fixation points
    pos = (0, 5) if position == 'top' else (0, -5)
    prime.pos = pos
    mask.pos = pos
    blur_region.pos = pos

    # Include fixation and wait text point to the prime
    prime = visual.BufferImageStim(win, stim=[prime, fixation])

    # Combine the two components of the mask and fixation and wait text together
    mask = visual.BufferImageStim(win, stim=[mask, blur_region, fixation])
    
    # Wait screen
    wait = visual.BufferImageStim(win, stim=[fixation])

    # Run frames
    if ISI != 0:
        frames = [wait, prime, wait, mask]
        frameDurations = [120, primeFrame, ISI, maskFrame]
        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)
        critTime = exlib.actualFrameDurations(frameDurations, stamps)[2]
        critPass = (np.absolute((ISI/refreshRate) - critTime) < .001)
        if not critPass:
            print('Critical pass fail at trial ' + str(trial_num) + ' : while critical time is ' + str(np.round(critTime, 4)) +
                  ', actual time is ' + str(np.round(ISI/refreshRate, 4)))
    else:
        frames = [wait, prime, mask]
        frameDurations = [120, primeFrame, maskFrame] 
        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)

    # Record the reaction time and wait for response for at most 1.5s
    trialClock.reset()
    fixation.draw()
    win.flip()
    keys = event.waitKeys(maxWait=5, timeStamped=trialClock, keyList=['x', 'm'])

    # Check if the response was correct
    if keys:
        key, rt = keys[0]
        response = 'left' if key == 'x' else 'right'
        correctness = (response == true)
    else:
        response, rt, correctness = None, None, False  # No response is considered incorrect

    # Provide feedback if it's a practice trial
    if provide_feedback:
        feedback_text = 'Correct!' if correctness else 'Incorrect!'
        feedback = visual.TextStim(win, text=feedback_text, pos=(0, 0), color = [-1, -1, -1], height = 0.7)
        feedback.draw()
        win.flip()
        core.wait(1)  # Display feedback for 1 second

    # 1-second break before the next fixation point
    else:
        win.flip()  # Clear the screen
        core.wait(0.2) # Display feedback for 0.2 second

    # Return trial result
    output = [pid,
              sid,
              goal,
              (block_num - 1) * num_trials_per_block + trial_num,
              block_num,
              trial_num,
              prime_direction, 
              mask_direction, 
              prime_direction == mask_direction,
              np.round(ISI * 0.006, 3), 
              position, 
              response, 
              np.round(rt, 3) if rt is not None else rt, 
              correctness]
    if provide_feedback == False:
        print(output)
        print(*output, sep=',', file=fptr)

# Define a function for a practice trial
def run_practice_block(n_trials=practice_num, goal = None):
    # Start the practice block
    start_practice_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    # Generate practice trial conditions (randomized)
    conditions = []
    for _ in range(n_trials):
        ISI = random.choice(ISI_frames)
        position = random.choice(['top', 'bottom'])
        prime_direction = random.choice(['left', 'right'])
        mask_direction = random.choice(['left', 'right'])
        conditions.append({'prime': prime_direction, 'mask': mask_direction, 'ISI': ISI, 'position': position})
    random.shuffle(conditions)

    # Run each trial in the practice block
    for trial_num, trial in enumerate(conditions):
        # Check for escape key to quit
        if 'escape' in event.getKeys():
            return True  # Signal to quit

        # Run the trial with feedback enabled
        run_trial(
            block_num=0,  # Block 0 for practice
            trial_num=trial_num + 1,
            prime_direction=trial['prime'],
            mask_direction=trial['mask'],
            ISI=trial['ISI'],
            position=trial['position'],
            provide_feedback=True,  # Enable feedback for practice
            goal = goal
        )

    # Show practice end message
    end_practice_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    return False  # Continue to the main experiment

# Define a function to run a block of trials
def run_block(block_num, n_trials_per_condition, ISI_frames, goal = None):
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
            block_num = block_num,
            trial_num = trial_num,
            prime_direction=trial['prime'],
            mask_direction=trial['mask'],
            ISI=trial['ISI'],
            position=trial['position'],
            goal = goal
        )

    return False  # Return results and signal to continue

# Define a function to run the full experiment with multiple blocks
def run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal = None):
    # Run the practice block firstcolor
    print("Running Practice Block...")
    quit_experiment = run_practice_block(goal = goal)
    if quit_experiment:
        print("Experiment quit by user during practice.")
        win.close()

    # Run the main experimental blocks
    for block_num in range(1, num_blocks + 1):
        print(f"Running Block {block_num}...")

        # Run a block of trials
        quit_experiment = run_block(block_num, n_trials_per_condition, ISI_frames, goal = goal)
        if quit_experiment:
            print("Experiment quit by user.")
            break  # Stop experiment if quit signal received

        # Pause between blocks (except last one)
        if block_num < num_blocks:
            break_text = visual.TextStim(win, text=f'Block {block_num} finished\nPress space to continue to the next block', pos=(0, 0), color=[-1, -1, -1])
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
mask_left.pos = (0,-5)
blur_region.pos = (0,-5)
mask_left.draw()
blur_region.draw()
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
prime_right.pos = (0,-5)
mask_left.pos = (0,-5)
blur_region.pos = (0,-5)
mask_left.draw()
blur_region.draw()
prime_right.draw()
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
exlib.stopExp(sid,hz,resX,resY,seed,dbConf)

win.close()
# Get everything in the store file and close the file
fptr.flush()
# endregion
