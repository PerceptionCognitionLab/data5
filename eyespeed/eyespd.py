import numpy as np
import pandas as pd
from scipy.fft import fft2, ifft2
from numpy import random
from psychopy import core, visual, event, sound
from PIL import Image

# Globals

correctSound1 = sound.Sound(500, secs=0.25)
correctSound2 = sound.Sound(1000, secs=0.25)
incorrectSound1 = sound.Sound(500, secs=0.5)
incorrectSound2 = sound.Sound(375, secs=0.5)

def playCorrectSound():
    correctSound1.play()
    core.wait(0.25)
    correctSound2.play()
    core.wait(0.25)

def playIncorrectSound():
    incorrectSound1.play()
    core.wait(0.5)
    incorrectSound2.play()

# Initialize random number generator

rng = np.random.default_rng(seed=np.random.randint(1, 1000))

# Window

win = visual.Window(units="pix", size=(750, 750), color=[-1, -1, -1], fullscr=True)

# Noise Function

def add_noise(chosen_ltr_image, image2, deltaFft):
    weight = 0.5
    g1 = fft2(chosen_ltr_image)
    g2 = fft2(image2)
    power = (weight * np.abs(g1) + (1 - weight) * np.abs(g2))
    N = len(chosen_ltr_image)
    d = chosen_ltr_image.shape
    noise = np.random.normal(0, 1, d) 
    gNoise = fft2(noise)
    noisy_image = np.real(ifft2(gNoise * power)) / N
    return noisy_image

# Function to draw a random monochrome letter

def rand_ltr(win, duration=2, deltaFft=1):
    mono_W = np.flip(np.array(Image.open('testW.png').convert("L"))) / 255.0
    mono_A = np.flip(np.array(Image.open('testA.png').convert("L"))) / 255.0
    mono_M = np.flip(np.array(Image.open('testM.png').convert("L"))) / 255.0
    mono_O = np.flip(np.array(Image.open('testO.png').convert("L"))) / 255.0
    letters = [("A", mono_A), ("W", mono_W), ("M", mono_M), ("O", mono_O)]
    select1 = rng.integers(0, 4)
    select2 = rng.integers(0, 4)
    chosen_letter, chosen_ltr_image = letters[1]
    _, image2 = letters[2]
    noisy_image = add_noise(chosen_ltr_image, image2, deltaFft)
    presentedImage = chosen_ltr_image + noisy_image
    presentedImage = np.clip(presentedImage, 0, 1)  
    stim = visual.ImageStim(win, image=presentedImage)
    stim.draw()
    win.flip()
    core.wait(duration)
    return chosen_letter

# Function to get the response

def getresponse(win, chosen_letter):
    prompt = visual.TextStim(win, text="What letter did you see?", color=[1, 1, 1], height=40)
    prompt.draw()
    win.flip()
    keys = event.waitKeys(keyList=['a', 'w', 'm', 'o'])
    response = keys[0] if keys else None
    responseupper = response.upper() if response else None
    
    correct = responseupper == chosen_letter

    if correct:
        playCorrectSound()
        feedback_text = "That's correct"
    else:
        playIncorrectSound()
        feedback_text = "That's incorrect"

    feedback = visual.TextStim(win, text=feedback_text, color=[1, 1, 1], height=40)
    feedback.draw()
    win.flip()
    core.wait(2)
    return correct


def doTrial(numTrials, block, initial_deltaFft):
    for blk in range(block):
        prompt = visual.TextStim(win, text="Press any key to continue", color=[1, 1, 1], height=40)
        prompt.draw()
        win.flip()
        event.waitKeys()
        chosen_letter_array = []
        correct_array = []
        deltaFft = initial_deltaFft
        consecutive_correct = 0
        
        for _ in range(numTrials):
            chosen_letter = rand_ltr(win, duration=2, deltaFft=deltaFft)
            print('Noise deltaFft:', deltaFft)
            correct = getresponse(win, chosen_letter)
            chosen_letter_array.append(chosen_letter)
            correct_array.append(correct)
            print('Randomly chosen letter:', chosen_letter)
            print('Correct response:', correct)
            
            if correct:
                consecutive_correct += 1
                if consecutive_correct == 2:
                    deltaFft *= np.sqrt(2)
                    consecutive_correct = 0
            else:
                consecutive_correct = 0
                deltaFft /= np.sqrt(2)
                
            deltaFft = max(deltaFft, 1)  

    return chosen_letter_array, correct_array

numTrials = 2
block = 1
initial_deltaFft = 1

chosen_letter_array, correct_array = doTrial(numTrials, block, initial_deltaFft)
print('Chosen letter array:', chosen_letter_array)
print('Response correctness:', correct_array)
win.close()
core.quit()