import numpy as np
from numpy import random
from psychopy import core, visual, event
from PIL import Image
import sys
import os
import time


# Initialize random number generator
rng = np.random.default_rng(seed=np.random.randint(1, 1000))

# Window
win = visual.Window(units="pix", size=(750, 750), color=[1, 1, 1], fullscr=True)

# Function to draw a random monochrome letter
def rand_ltr(win, duration=2):
    mono_W = np.flip(np.array(Image.open('testW.png').convert("L"))) / 255.0
    mono_A = np.flip(np.array(Image.open('testA.png').convert("L"))) / 255.0
    mono_M = np.flip(np.array(Image.open('testM.png').convert("L"))) / 255.0
    mono_O = np.flip(np.array(Image.open('testO.png').convert("L"))) / 255.0
    letters = [("A", mono_A), ("W", mono_W), ("M", mono_M), ("O", mono_O)]
    select = rng.integers(0, 4)
    chosen_letter, chosen_ltr_image = letters[select]
    stim = visual.ImageStim(win, image=chosen_ltr_image)
    stim.draw()
    win.flip()
    core.wait(duration)
    return chosen_letter

# Function to get the response
def getresponse(win, chosen_letter):
    prompt = visual.TextStim(win, text="What letter did you see?", color=[-1, -1, -1], height = 40)
    prompt.draw()
    win.flip()
    keys = event.waitKeys()
    response = keys[0] if keys else None
    responseupper = response.upper()
    
    correct = responseupper == chosen_letter

    if correct:
        feedback_text = "That's correct"
    else:
        feedback_text = "That's incorrect"

    feedback = visual.TextStim(win, text=feedback_text, color=[-1, -1, -1], height = 40)
    feedback.draw()
    win.flip()
    core.wait(2)

    return correct

# Run the test
chosen_letter = rand_ltr(win, duration=2)
correct = getresponse(win, chosen_letter)
print('Randomly chosen letter:', chosen_letter)
print('Correct response:', correct)
win.close()
core.quit()


