# Imports
from psychopy import core, visual, sound, event
import random
import numpy as np
import csv
import sys

refreshRate = 165

sid = 1
pid = 1

win = visual.Window(units="pix", size=(800, 600), color=[-1, -1, -1], fullscr=True)
mouse = event.Mouse(visible=False, newPos=[0, 0], win=win)  # Mouse centered at zero
trialClock = core.Clock()
seed = random.randrange(1e6)
random.seed(seed)

# Fixation cross
fix = visual.TextStim(win, "+", color=[1, 1, 1])  # White fixation cross

# Global parameters for loud vs. soft task
base_frequency = 1000  # Base frequency for all tones (constant)
initial_amplitude_diff_fraction = 0.5  # Initial amplitude difference as a fraction
minimum_amplitude_diff_fraction = 0.1  # Minimum amplitude difference as a fraction
tone_duration = 0.4  # Duration of each tone in seconds
silence_duration = 0.2  # Duration of silence between tones
max_trials = 5  # Maximum number of trials

# Instructions
instructions = visual.TextStim(win, text="In this experiment, you will be presented with two tones.\n"
                                         "Your job is to determine whether the second tone is louder or softer compared to the first tone.\n"
                                         "Press '1' if you think the first tone is louder. Press '2' if you think the second tone is louder.\n"
                                         "Press any key to start.", color=[1, 1, 1])
instructions.draw()
win.flip()
event.waitKeys()

# Function to generate and play a tone
def play_tone(frequency, duration, amplitude):
    tone = sound.Sound(frequency, secs=duration)
    tone.setVolume(amplitude)
    tone.play()
    core.wait(duration)

# Data storage
data_filename = f'subject_{sid}_data.csv'
data_file = open(data_filename, 'w')
data_file.write('Trial,FirstToneAmplitude,SecondToneAmplitude,CorrectResponse,ParticipantResponse,RT\n')

# Run trials
amplitude_diff_fraction = initial_amplitude_diff_fraction
amplitude_diff_decrease_step = (initial_amplitude_diff_fraction - minimum_amplitude_diff_fraction) / max_trials

for trial in range(max_trials):
    base_amplitude = 0.5  # Base amplitude (scaled down for safety)
    amplitude_diff = base_amplitude * amplitude_diff_fraction
    first_tone_amp = base_amplitude
    second_tone_amp = base_amplitude + amplitude_diff if random.random() > 0.5 else base_amplitude - amplitude_diff
    correct_response = 2 if second_tone_amp > first_tone_amp else 1

    # Play first tone
    play_tone(base_frequency, tone_duration, first_tone_amp)
    core.wait(silence_duration)
    # Play second tone
    play_tone(base_frequency, tone_duration, second_tone_amp)

    # Collect response
    response_clock = core.Clock()
    keys = event.waitKeys(keyList=['1', '2'], timeStamped=response_clock)
    if keys:
        participant_response, rt = keys[0]
        participant_response = int(participant_response)

    # Save data
    data_file.write(f'{trial},{first_tone_amp},{second_tone_amp},{correct_response},{participant_response},{rt}\n')
    print(data_file)

    # Feedback
    if participant_response == correct_response:
        feedback = visual.TextStim(win, text="Correct!", color='green')
    else:
        feedback = visual.TextStim(win, text="Incorrect", color='red')
    feedback.draw()
    win.flip()
    core.wait(1)

    # Display progress
    progress_text = f'Trial {trial + 1}/{max_trials}'
    progress = visual.TextStim(win, text=progress_text, color='white')
    progress.draw()
    win.flip()
    core.wait(1)

    # Decrease the amplitude difference for the next trial
    amplitude_diff_fraction = max(amplitude_diff_fraction - amplitude_diff_decrease_step, minimum_amplitude_diff_fraction)

# Close data file
data_file.close()

# End of experiment
thanks = visual.TextStim(win, text="Thank you for participating!\nPress any key to exit.", color=[1, 1, 1])
thanks.draw()
win.flip()
event.waitKeys()
win.close()
core.quit()