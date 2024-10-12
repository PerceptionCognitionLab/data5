import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import random
from psychopy import visual, core, event, prefs
import expLib51 as exlib
import numpy as np
import os
# In this pilot experiment, we aim to find the type B U shape metacontrast masking effect, we fixed the prime duration to be 7 frames (42ms) and ISI changes 
# among 0, 3, 6, and 9 frames (0ms, 18ms, 36ms, 54ms), each block has 6 * 3 * 2 * 4 = 144 trials, there will be 3 blocks in total 

# Housekeeping
# region
refreshRate=165
exlib.setRefreshRate(refreshRate)
trialClock=core.Clock()
expName="mp1"
dbConf=exlib.data5
seed = random.randrange(1e6)
#[pid,sid,fname]=exlib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname] = [1,1,'test.dat']
fptr = open(fname,'w')
# endregion

# Experiment settings
# region
num_blocks = 3
n_trials_per_condition = 3
ISI_frames = [0,3,6,9,12,18]
num_trials_per_block = 144
primeFrame = 7
maskFrame = 7
# endregion

# Define stimuli: primes, masks, text
#region
# Color
bg_color = [1,1,1]
sti_color = [-1,-1,-1]

# Set up the window
win = visual.Window(units="pix", size=(1920, 1080), color= [1,1,1], fullscr=True)

# Text stimuli
welcome_text = visual.TextStim(win, text='In this experiment, you will see a small white arrow followed by a large white arrow shown at either the upper or lower area of the screen.\n\nBelow is the sample stimuli of the small right arrow and big left arrow. The small white arrow locates at the center of the big white arrow. In the real experiment, the small arrow will appear shortly before the big arrow appear and disappear very quick.\n\n Your task is to identify the orientation of the first small arrow by pressing either x (for left) or m (for right).\n\nYour eyes should focus at the center fixation point. Once you make a judgement, the next pair of arrows will appear, keep doing the judgement until the block is over. There will be in total 3 blocks.\n\nThe experiment will last about 10 minutes. It is hard so try your best on orientation discrimination. Press space to start the experiment.', pos=(0, 100), color=sti_color)
goodbye_text = visual.TextStim(win, text='Experiment finished!\nThank you for your participation\nPress space to exit', pos=(0, 0), color=sti_color)

# Fixation and blank
fixation = visual.TextStim(win, text='+', pos=(0, 0), color=bg_color, bold = True, height = 40)

prime_left = visual.ShapeStim(
    win=win, vertices=[(-90,0),(-70,20),(80,20),(60,0),(80,-20),(-70,-20)],
    fillColor=sti_color , lineColor=sti_color , size=1)
prime_right = visual.ShapeStim(
    win=win, vertices=[(-60,0),(-80,20),(70,20),(90,0),(70,-20),(-80,-20)],
    fillColor=sti_color , lineColor=sti_color , size=1)
mask_left = visual.ShapeStim(
    win=win, vertices=[(-165, 0), (-120, 45), (120, 45), (120, -45), (-120, -45)],
    fillColor=sti_color , lineColor=sti_color , size=1)
mask_right = visual.ShapeStim(
    win=win, vertices=[(-120, 45), (120, 45), (165,0), (120, -45), (-120, -45)],
    fillColor=sti_color , lineColor=sti_color , size=1)
mask_inner = visual.ShapeStim(
    win=win, vertices=[(-105,30),(105,30),(90,15),(105,0),(90,-15),(105,-30),(-105,-30),(-90,-15),(-105,0),(-90,15)],
    fillColor=bg_color, lineColor=bg_color, size=1)
#endregion

# Define a function for a single trial
def run_trial(block_num, trial_num, prime_direction, mask_direction, ISI, position, provide_feedback=False): 
    # Set the orientation of the prime used in this trial
    prime = prime_left if prime_direction == 'left' else prime_right
    mask_outer = mask_left if mask_direction == 'left' else mask_right
    
    # Set position for both prime and mask either at top or bottom of the fixation points
    pos = (0, 130) if position == 'top' else (0, -130)
    prime.pos = pos
    mask_outer.pos = pos
    mask_inner.pos = pos

    # Include fixation and wait text point to the prime
    prime = visual.BufferImageStim(win, stim=[prime, fixation])

    # Combine the two components of the mask and fixation and wait text together
    mask = visual.BufferImageStim(win, stim=[mask_outer, mask_inner, fixation])
    
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
        correctness = (response == prime_direction)
    else:
        response, rt, correctness = None, None, False  # No response is considered incorrect

    # Provide feedback if it's a practice trial
    if provide_feedback:
        feedback_text = 'Correct!' if correctness else 'Incorrect!'
        feedback = visual.TextStim(win, text=feedback_text, pos=(0, 0), color=sti_color)
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
def run_practice_block(n_trials=20):
    # Start the practice block
    start_practice_text = visual.TextStim(win, text='We will begin with some practice trials. We will provide feedback on correctness. Note that in the real experiment there will be no feedback.\n\nPress space to start the practice trials.', pos=(0, 0), color=sti_color)
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
            provide_feedback=True  # Enable feedback for practice
        )

    # Show practice end message
    end_practice_text = visual.TextStim(win, text='Practice finished.\nPress space to start the real experiment.', pos=(0, 0), color=sti_color)
    end_practice_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    return False  # Continue to the main experiment

# Define a function to run a block of trials
def run_block(block_num, n_trials_per_condition, ISI_frames):
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
            position=trial['position']
        )

    return False  # Return results and signal to continue

# Define a function to run the full experiment with multiple blocks
def run_experiment(num_blocks, n_trials_per_condition, ISI_frames):
    # Run the practice block first
    print("Running Practice Block...")
    quit_experiment = run_practice_block()
    if quit_experiment:
        print("Experiment quit by user during practice.")
        return

    # Run the main experimental blocks
    for block_num in range(1, num_blocks + 1):
        print(f"Running Block {block_num}...")

        # Run a block of trials
        quit_experiment = run_block(block_num, n_trials_per_condition, ISI_frames)
        if quit_experiment:
            print("Experiment quit by user.")
            break  # Stop experiment if quit signal received

        # Pause between blocks (except last one)
        if block_num < num_blocks:
            break_text = visual.TextStim(win, text=f'Block {block_num} finished\nPress space to continue to the next block', pos=(0, 0), color=sti_color)
            break_text.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

# The experiment skeleton
# region
# Welcome page
prime_right.pos = (0,-300)
mask_left.pos = (0,-300)
mask_inner.pos = (0,-300)
welcome_page = visual.BufferImageStim(win, stim=[welcome_text, mask_left, mask_inner,prime_right])
welcome_page.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Run the experiment
all_results = run_experiment(num_blocks, n_trials_per_condition, ISI_frames)

# Show goodbye screen
goodbye_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Record settings and close the window
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
#exlib.stopExp(sid,hz,resX,resY,seed,dbConf)

win.close()
# Get everything in the store file and close the file
fptr.flush()
# endregion


