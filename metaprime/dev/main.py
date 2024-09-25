from psychopy import visual, core, event, data, gui, logging
import random

# Set up the window
win = visual.Window(units="pix", size=(500, 500), color='grey', fullscr=True)

# Define the properties of the prime (small arrow)
prime_left = visual.ShapeStim(
    win=win, vertices=[(-30, 15), (30, 15), (30, -15), (-30, -15),(-50, 0)], 
    fillColor="black", lineColor="black", pos=(0, 100), size=1)
prime_right = visual.ShapeStim(
    win=win, vertices=[(-30, 15), (30, 15), (50, 0), (30, -15), (-30, -15)], 
    fillColor="black", lineColor="black", pos=(0, 100), size=1)

# Define the properties of the mask (large arrow with cut-out)
mask_left = visual.ShapeStim(
    win=win, vertices=[(-60, 20), (60, 20), (60, -20), (-60, -20),(-80, 0)], 
    fillColor="black", lineColor="black", pos=(0, 100), size=1)
mask_right = visual.ShapeStim(
    win=win, vertices=[(-60, 20), (60, 20), (80, 0), (60, -20), (-60, -20)], 
    fillColor="black", lineColor="black", pos=(0, 100), size=1)
mask_inner = visual.ShapeStim(
    win=win, vertices=[(-50, 10), (50, 10), (50, -10), (-50, -10)], 
    fillColor="white", lineColor="white", pos=(0, 100), size=1)

# Create welcome screen text
welcome_text = visual.TextStim(win, text='Welcome to the experiment\nPress space to continue', pos=(0, 0), color="black")

# Create instruction screen text
instruction_text = visual.TextStim(
    win=win, text='Instructions:\nYou will see an arrow on either at the top or the bottom of the screen\nYour task is to identify the direction of the arrow as fast as you can.\nUse the left or right arrow keys to indicate your choice', 
    pos=(0, 0), color="black"
)

# Create goodbye screen text
goodbye_text = visual.TextStim(win, text='Experiment finished!\nThank you for your participation\nPress space to exit', pos=(0, 0), color="black")

# Function to run a block of trials
def run_block(n_trials_per_condition=5, soa_list=[14, 28, 42, 56, 70, 84]):
    # Generate conditions (SOA, prime, mask combinations)
    conditions = []
    for soa in soa_list:
        for position in ['top', 'bottom']:  # Add both top and bottom conditions
            conditions.append({'soa': soa, 'prime': 'left', 'mask': 'left', 'position': position})
            conditions.append({'soa': soa, 'prime': 'right', 'mask': 'right', 'position': position})
            conditions.append({'soa': soa, 'prime': 'left', 'mask': 'right', 'position': position})
            conditions.append({'soa': soa, 'prime': 'right', 'mask': 'left', 'position': position})

    # Create a randomized trial list
    trial_list = conditions * n_trials_per_condition
    random.shuffle(trial_list)

    # Create a clock to record reaction time for each trial
    trial_clock = core.Clock()
    results = []  # Store results for each trial

    # Main experiment loop for this block
    for trial in trial_list:
        # Check if the escape key is pressed to quit the experiment
        if 'escape' in event.getKeys():
            return results, True  # Return immediately, signal to quit the entire experiment

        # Set the position for the prime and mask based on the trial
        if trial['position'] == 'top':
            prime_pos = (0, 100)
            mask_pos = (0, 100)
        else:
            prime_pos = (0, -100)
            mask_pos = (0, -100)

        # Update the position of prime and mask stimuli
        prime_left.pos = prime_pos
        prime_right.pos = prime_pos
        mask_left.pos = mask_pos
        mask_right.pos = mask_pos
        mask_inner.pos = mask_pos

        # Show fixation cross for 700 ms
        fixation = visual.TextStim(win, text='+', pos=(0, 0), color="black")
        fixation.draw()
        win.flip()
        core.wait(0.7)

        # Show prime (small arrow) for 14 ms
        if trial['prime'] == 'left':
            prime_left.draw()
        else:
            prime_right.draw()
        win.flip()
        core.wait(0.014)

        # Show a blank screen for the SOA duration (prime disappears, then mask appears after SOA)
        win.flip()
        core.wait(trial['soa'] / 1000.0)

        # Show mask for 140 ms
        if trial['mask'] == 'left':
            mask_left.draw()
            mask_inner.draw()
        else:
            mask_right.draw()
            mask_inner.draw()
        win.flip()

        # Record the reaction time and start the clock
        trial_clock.reset()

        # Wait for participant response, or timeout after 1.5 seconds
        keys = event.waitKeys(maxWait=1.5, keyList=['left', 'right'], timeStamped=trial_clock)

        # Check if the response was correct
        if keys:
            key, rt = keys[0]
            correct = (key == trial['mask'])  # Correct if the key matches the mask direction
        else:
            key, rt, correct = None, None, False  # No response is considered incorrect

        # Save the trial results
        results.append({'soa': trial['soa'], 'prime': trial['prime'], 'mask': trial['mask'], 
                        'position': trial['position'], 'response': key, 'rt': rt, 'correct': correct})

    return results, False  # Continue the experiment if no escape

# Show the welcome screen and wait for space key press to continue
welcome_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Function to run multiple blocks
def run_experiment(num_blocks, n_trials_per_condition=5, soa_list=[14, 28, 42, 56, 70, 84]):
    all_results = []
    for block_num in range(num_blocks):
        print(f"Running Block {block_num + 1}...")
        results, quit_experiment = run_block(n_trials_per_condition, soa_list)
        all_results.extend(results)  # Combine all results from each block

        if quit_experiment:  # Check if Escape was pressed
            print("Experiment quit by user.")
            break  # Break out of the block loop and quit the entire experiment

        # Optional: Pause between blocks, and allow a break
        if block_num < num_blocks - 1:  # Skip pause for the last block
            break_text = visual.TextStim(win, text=f'Block {block_num + 1} finished\nPress space to continue to the next block', pos=(0, 0), color="black")
            break_text.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

    return all_results

# Run the experiment with a specified number of blocks
num_blocks = 3  # Example: run 3 blocks
all_results = run_experiment(num_blocks)

# Show the goodbye screen and wait for space key press to exit
goodbye_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Close the window after the experiment ends
win.close()

# Print results to the console
for result in all_results:
    print(result)


