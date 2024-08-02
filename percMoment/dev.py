from psychopy import sound, visual, core, event, data, logging
import numpy as np
import random
import os

# Global parameters
subjid = 1  # Subject ID
random.seed(subjid)  # Set random seed
base_frequencies = [500, 750, 1250]  # Base frequencies to test
starting_freq_diff_fraction = 0.25  # Starting frequency difference as a fraction
tone_duration = 0.4  # Duration of each tone in seconds
silence_duration = 0.2  # Duration of silence between tones
num_training_trials = 5  # Number of training trials
num_reversals_to_stop = 6  # Number of reversals before stopping
num_incorrect_to_stop = 3  # Number of incorrect responses before stopping training
max_trials = 100  # Maximum number of trials

# Set up PsychoPy window
win = visual.Window([800, 600], color='white', units='pix')

# Instructions
instructions = visual.TextStim(win, text="In this experiment, you will be presented with two tones.\n"
                                          "Your job is to determine whether the second tone is higher or lower in pitch compared to the first tone.\n"
                                          "Press '1' if you think the second tone is higher and '2' if you think the second tone is lower.\n"
                                          "Press any key to start.")
instructions.draw()
win.flip()
event.waitKeys()

# Function to generate and play a tone
def play_tone(frequency, duration):
    tone = sound.Sound(frequency, secs=duration, sampleRate=44100)
    tone.play()
    core.wait(duration)

# Data storage
data_filename = f'subject_{subjid}_data.csv'
data_file = open(data_filename, 'w')
data_file.write('Trial,BaseFrequency,FirstTone,SecondTone,CorrectResponse,ParticipantResponse,RT\n')

# Run trials
for trial in range(max_trials):
    base_freq = random.choice(base_frequencies)
    freq_diff = base_freq * starting_freq_diff_fraction
    first_tone_freq = base_freq
    second_tone_freq = base_freq + freq_diff if random.random() > 0.5 else base_freq - freq_diff
    correct_response = 1 if second_tone_freq > first_tone_freq else 2

    # Play first tone
    play_tone(first_tone_freq, tone_duration)
    core.wait(silence_duration)
    # Play second tone
    play_tone(second_tone_freq, tone_duration)
    
    # Collect response
    response_clock = core.Clock()
    keys = event.waitKeys(keyList=['1', '2'], timeStamped=response_clock)
    if keys:
        participant_response, rt = keys[0]
        participant_response = int(participant_response)

    # Save data
    data_file.write(f'{trial},{base_freq},{first_tone_freq},{second_tone_freq},{correct_response},{participant_response},{rt}\n')

    # Feedback
    if participant_response == correct_response:
        feedback = visual.TextStim(win, text="Correct!", color='green')
    else:
        feedback = visual.TextStim(win, text="Incorrect", color='red')
    feedback.draw()
    win.flip()
    core.wait(1)

# Close data file
data_file.close()

# End of experiment
thanks = visual.TextStim(win, text="Thank you for participating!\nPress any key to exit.")
thanks.draw()
win.flip()
event.waitKeys()
win.close()
core.quit()
