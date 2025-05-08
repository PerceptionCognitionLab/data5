import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import random
from psychopy import visual, core, event, prefs
import expLib51 as exlib
import numpy as np
import os
from psychopy import visual, core, monitors

# Housekeeping
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
# region
monitor = monitors.Monitor("MyMonitor")
monitor.setSizePix((1920, 1080))
monitor.setWidth(53.1)
monitor.setDistance(100)
monitor.saveMon()
# endregion

# Experiment settings
# region
num_blocks = 3
n_trials_per_condition = 3
ISI_frames = [0, 4, 8, 12, 16, 20]
mask_practice_frames = [4,8,12]
prime_practice_frames = [0,20]
num_trials_per_block = 144
primeFrame = 2
maskFrame = 7 
gapFrame = 120
gap = 0.2
practice_num = 20
# endregion

# Stimulus settings
# region
pos_text = (0,3.5)
ori_left = -45
ori_right = 45
prime_size = 3
mask_size = 4.5
blur_size = 7.2
text_height = 0.5
stimulus_contrast = 0.75
blur_contrast = 0.2
sf = 0.75
text_color = [-1,-1,-1]
bg_color = [0, 0, 0]
win_size = (1920, 1080)
pos_top = (0,5)
pos_bottom = (0,-5)
# endregion

# Define stimuli
#region
# Set up the window
win = visual.Window(units="deg", monitor = monitor, size=win_size, color= bg_color, fullscr=True)

# Text stimulus
fixation = visual.TextStim(win, text='+', pos=(0, 0), color = text_color, bold = True, height = 0.7)
prime_left = visual.GratingStim(win=win,tex = "sin", size = prime_size, sf = sf, ori = ori_left, contrast = stimulus_contrast, mask = 'gauss')
prime_right = visual.GratingStim(win=win,tex = "sin", size = prime_size, sf = sf, ori = ori_right, contrast = stimulus_contrast, mask = 'gauss')
mask_left = visual.GratingStim(win=win,tex = "sin", size = mask_size, sf = sf, ori = ori_left, contrast = stimulus_contrast, mask = 'circle')
mask_right = visual.GratingStim(win=win,tex = "sin", size = mask_size, sf = sf, ori = ori_right, contrast = stimulus_contrast, mask = 'circle')
blur_region = visual.GratingStim(win = win,tex = None,  size= blur_size,  sf = 0,   mask = "gauss",  color = bg_color, contrast = blur_contrast)
#endregion 

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
    pos = pos_top if position == 'top' else pos_bottom
    prime.pos = pos
    mask.pos = pos
    blur_region.pos = pos

    # Set stimulus
    prime = visual.BufferImageStim(win, stim=[prime, fixation])
    mask = visual.BufferImageStim(win, stim=[mask, blur_region, fixation])
    wait = visual.BufferImageStim(win, stim=[fixation])

    # Run frames
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
    output = [pid,sid,goal,(block_num - 1) * num_trials_per_block + trial_num,block_num,trial_num,prime_direction, mask_direction, prime_direction == mask_direction,np.round(ISI * 0.006, 3), position, response, np.round(rt, 3) if rt is not None else rt, correctness]
    if provide_feedback == False:
        print(output)
        print(*output, sep=',', file=fptr)

# Define a function for a practice trial
def run_practice_block(n_trials=practice_num, goal = None):
    # Generate practice trial conditions (randomized)
    if goal == 'mask':
        ISI_frames = mask_practice_frames
    else:
        ISI_frames = prime_practice_frames
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
        run_trial(block_num=0,  trial_num=trial_num + 1,prime_direction=trial['prime'],mask_direction=trial['mask'],ISI=trial['ISI'],position=trial['position'],provide_feedback=True,  goal = goal)
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
            break_text = visual.TextStim(win, text=f'Block {block_num} finished\nPress space to continue to the next block (three blocks in total)', pos=(0, 0), color=[-1, -1, -1])
            break_text.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

# The experiment skeleton

# Instruction text
# region
welcome_text1 = visual.TextStim(win, text='Welcome to the experiment! Press space to continue.', height = text_height, pos = pos_text , color = 'black')
welcome_text2 = visual.TextStim(win, text='The experiment contains two sessions. Each session has three blocks and lasts around 15 minutes.\n\nPress space to start the instrution for the first session.', height = text_height, pos = pos_text , color = text_color)
mask_text1 = visual.TextStim(win, text='The picture shown below is called a grating, its orientation is up-to-the-left.\n\nPress space to continue', height = text_height, pos = pos_text, color = text_color)
mask_text2 = visual.TextStim(win, text='Here is another grating with different orientation. This grating is up-to-the-right', height = text_height, pos = pos_text, color = text_color)
mask_text3 = visual.TextStim(win, text='In the following task, these two gratings will flash quickly on the screen, your task is to identify the orientation of the grating.\n\nUse keyboard to make your decision.\n\n If you think the grating is oriented up-to-the-left, press X. If it is orientated up-to-the-right, press M.\n\nPress space to continue', height = text_height, pos = pos_text, color = text_color)
mask_text4 = visual.TextStim(win, text='We will give you some easy practice trials first, feedback on corretness will be given after each trial.\n\nPress space to start the practice trial', height = text_height, pos = pos_text, color = text_color)
mask_text5 = visual.TextStim(win, text='Excellent! Now we will start the main experiment, no feedback on corretness will be given. The task will be a little more difficult than the practice trial.\n\nYou may see something flash before the grating, please ignore it and focus on discriminating the orientation of the grating.\n\nPress space to start the mian experiment', height = text_height, pos = pos_text, color = text_color)

rest_text=  visual.TextStim(win, text='Session 1 ends! You may take a break before starting session 2.\n\nPress space to continue.', height = text_height, pos = pos_text , color = text_color)

prime_text1 = visual.TextStim(win, text='You may or may not have notice that there is a smaller grating appears at the center of the bigger grating.\n\nBelow is an example where the bigger grating and smaller grating has the opposite direction. The bigger grating is orientated up-to-the-left, the smaller grating is orientated up-to-the-right\n\nPress space to continue', height = text_height, pos = pos_text, color = text_color)
prime_text2 = visual.TextStim(win, text='Here is another example, where both the smaller and bigger gratings are oriented up-to-the left.\n\nPress space to continue', height = text_height, pos = pos_text, color = text_color)
prime_text3 = visual.TextStim(win, text='This time, your task is to identify the orientation of the smaller grating. Try your best to ignore the interruption from the bigger grating.\n\n If you think the grating is oriented up-to-the-left, press X. If it is orientated up-to-the-right, press M.\n\nPress space to continue \n\nPress space to continue', height = text_height, pos = pos_text, color = text_color)
prime_text4 = visual.TextStim(win, text='We will give you some easy practice trials first, feedback on corretness will be given after each trial.\n\nPress space to start the practice trial', height = text_height, pos = pos_text, color = text_color)
prime_text5 = visual.TextStim(win, text='Excellent! Now we will start the main experiment, no feedback on corretness will be given. The main task is more difficult than the practice trial. Please try you best!\n\nPress space to start the mian experiment', height = text_height, pos = pos_text, color = text_color)

goodbye_text = visual.TextStim(win, text='Experiment finished! Thank you for participating!\n\nPress spacebar to exit', height = text_height, pos = pos_text , color = 'black')
# endregion

# Workflow
# region
# welcome
welcome_text1.draw()
win.flip()
event.waitKeys(keyList=['space'])

welcome_text2.draw()
win.flip()
event.waitKeys(keyList=['space'])

# instruction for mask trial
mask_left.pos = pos_bottom
blur_region.pos = pos_bottom
mask_left.draw()
blur_region.draw()
mask_text1.draw()    option = get_input("Change settings?\n1.No change\n2.Change orientaion\n3.Change spatial frequency\n4.Change contrast\n5.Change phase\n6.Chnage frames\n7.Change pr
win.flip()
event.waitKeys(keyList=['space'])

mask_right.pos = pos_bottom
blur_region.pos = pos_bottom
mask_left.draw()
blur_region.draw()
mask_text2.draw()
win.flip()
event.waitKeys(keyList=['space'])

mask_text3.draw()
win.flip()
event.waitKeys(keyList=['space'])

mask_text4.draw()
win.flip()
event.waitKeys(keyList=['space'])

quit_experiment = run_practice_block(goal = 'mask')
if quit_experiment:
    win.close()

mask_text5.draw()
win.flip()
event.waitKeys(keyList=['space'])
all_results = run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal = 'mask')

# rest
rest_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# instruction for prime trial
prime_right.pos = pos_bottom
mask_left.pos = pos_bottom
blur_region.pos = pos_bottom
mask_left.draw()
blur_region.draw()
prime_right.draw()
prime_text1.draw()
win.flip()
event.waitKeys(keyList=['space'])

prime_left.pos = pos_bottom
mask_left.pos = pos_bottom
blur_region.pos = pos_bottom
mask_left.draw()
blur_region.draw()
prime_right.draw()
prime_text1.draw()
win.flip()
event.waitKeys(keyList=['space'])

prime_text3.draw()
win.flip()
event.waitKeys(keyList=['space'])

prime_text4.draw()
win.flip()
event.waitKeys(keyList=['space'])

quit_experiment = run_practice_block(goal = 'prime')
if quit_experiment:
    win.close()

prime_text5.draw()
win.flip()
event.waitKeys(keyList=['space'])
all_results = run_experiment(num_blocks, n_trials_per_condition, ISI_frames, goal = 'prime')

# Show goodbye screen
goodbye_text.draw()
win.flip()
event.waitKeys(keyList=['space'])
# endregion

# Record settings and close the window
hz=round(win.getActualFrameRate())
[resX,resY]=win.size
exlib.stopExp(sid,hz,resX,resY,seed,dbConf)
win.close()
# Get everything in the store file and close the file
fptr.flush()

