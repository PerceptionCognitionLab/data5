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

win = visual.Window(units="pix", size=(750, 750), color=[-1, -1, -1], fullscr=True)

# Noise Function

def add_noise(image,mean = 0,stddev = 2): ### need to make a function that adjusts the standard devision based on correctness
    noise = random.normal(mean,stddev,image.shape)
    noisy_image = np.clip(image + noise,0,1)
    return(noisy_image)

# Function to draw a random monochrome letter

def rand_ltr(win, duration=2, stddev=2):
    mono_W = np.flip(np.array(Image.open('testW.png').convert("L"))) / 255.0 ### add a for loop and collect an array of images generated
    mono_A = np.flip(np.array(Image.open('testA.png').convert("L"))) / 255.0
    mono_M = np.flip(np.array(Image.open('testM.png').convert("L"))) / 255.0
    mono_O = np.flip(np.array(Image.open('testO.png').convert("L"))) / 255.0
    letters = [("A", mono_A), ("W", mono_W), ("M", mono_M), ("O", mono_O)]
    select = rng.integers(0, 4)
    chosen_letter, chosen_ltr_image = letters[select]
    noisy_image = add_noise(chosen_ltr_image, mean = 0, stddev=stddev)
    stim = visual.ImageStim(win, image=noisy_image)
    stim.draw()
    win.flip()
    core.wait(duration)
    return chosen_letter

# Function to get the response

def getresponse(win, chosen_letter):
    prompt = visual.TextStim(win, text="What letter did you see?", color=[1, 1, 1], height = 40)
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

    feedback = visual.TextStim(win, text=feedback_text, color=[1, 1, 1], height = 40)
    feedback.draw()
    win.flip()
    core.wait(2)
    return correct

# Run the test

def doTrial(numTrials):
    chosen_letter_array = []
    correct_array = []
    correct = False
    stddev = 3
    c = 0
    for i in range(numTrials):
        if correct:
            c = c + 1
            if c == 2:
                stddev = stddev + 1
                c = 0
        else:
            stddev = stddev - 1
            if stddev < 1:
                stddev = 1
        

        chosen_letter = rand_ltr(win, duration=2, stddev = stddev)
        print('Noise as a function of standard deviation per trial:',stddev)
        correct = getresponse(win, chosen_letter)
        chosen_letter_array.append(chosen_letter)
        correct_array.append(correct)
        print('Randomly chosen letter:', chosen_letter)
        print('Correct response:', correct)
    return chosen_letter_array, correct_array


numTrials = 5

chosen_letter_array, correct_array = doTrial(numTrials)
print('Chosen letter array:', chosen_letter_array)
print('Response correctness:', correct_array)
win.close()
core.quit()

