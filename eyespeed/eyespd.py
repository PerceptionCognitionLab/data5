import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fftn, ifftn
from numpy import random
from psychopy import core, visual, event, sound
from PIL import Image
import os

# Globals
abortKey = ['9']
correctSound1 = sound.Sound(500, secs=0.25)
correctSound2 = sound.Sound(1000, secs=0.25)
incorrectSound1 = sound.Sound(500, secs=0.5)
incorrectSound2 = sound.Sound(375, secs=0.5)
rng = np.random.default_rng(seed=np.random.randint(1, 1000))
win = visual.Window(units="pix", size=(1920, 1080), color=[-1, -1, -1], fullscr=True)
clock = core.Clock()

# Functions
def playCorrectSound():
    correctSound1.play()
    core.wait(0.25)
    correctSound2.play()
    core.wait(0.25)

def playIncorrectSound():
    incorrectSound1.play()
    core.wait(0.5)
    incorrectSound2.play()

def rand_ltr(win, duration=2, noise_std=1):
    m = np.array(Image.open('testM.png').convert('L')) / 255
    w = np.array(Image.open('testW.png').convert('L')) / 255
    a = np.array(Image.open('testA.png').convert('L')) / 255
    o = np.array(Image.open('testO.png').convert('L')) / 255

    letters = {'a': a, 'w': w, 'm': m, 'o': o}

    chosen_letter = rng.choice(list(letters.keys()))
    chosen_image = letters[chosen_letter]
    other_image = rng.choice(list(letters.values()))
    image2 = rng.choice(list(letters.keys()))

    d = chosen_image.shape
    weight = round(rng.uniform(.25,.75), 4)
    g1 = fftn(chosen_image)
    g2 = fftn(other_image)

    power = (weight * np.abs(g1) + (1 - weight) * np.abs(g2))
    noise = np.random.normal(loc=0, scale=noise_std, size=d)
    gNoise = fftn(noise)
    fNoise = np.real(ifftn(gNoise * power))
    stimuli = fNoise + 50 * chosen_image

    temp_image_path = "temp_stimulus.png"
    plt.imsave(temp_image_path, stimuli, cmap='gray')

    fix = visual.TextStim(win, "+") 
    fix.draw()
    win.flip()
    core.wait(.5)
    stim = visual.ImageStim(win, image=temp_image_path, size=(800, 600))
    stim.draw()
    win.flip()
    core.wait(duration)

    os.remove(temp_image_path)

    return chosen_letter, image2, weight

def getresponse(win, chosen_letter):
    prompt = visual.TextStim(win, text="What image did you see?", color=[1, 1, 1], height=40)
    prompt.draw()
    win.flip()
    keys = event.waitKeys(keyList=['a', 'w', 'm', 'o'])
    response = keys[0] if keys else None
    
    correct = response == chosen_letter

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

def doTrial(numTrials, block, noise_std):
    for blk in range(block):
        prompt = visual.TextStim(win, text="Press any key to continue", color=[1, 1, 1], height=40)
        prompt.draw()
        win.flip()
        event.waitKeys()
        
        chosen_letter_array = []
        image2_array = []
        correct_array = []
        std_array = []
        weights = []
        noise_std = 1.5
        consecutive_correct = 0
        deltaStd = 0.20

        for trl in range(numTrials):
            chosen_letter, image2, weight = rand_ltr(win, duration=2, noise_std=noise_std)
            correct = getresponse(win, chosen_letter)
            chosen_letter_array.append(chosen_letter)
            correct_array.append(correct)
            std_array.append(noise_std)
            image2_array.append(image2)
            weights.append(weight)
           
         
            if correct:
                consecutive_correct += 1
                if consecutive_correct == 2:
                    noise_std += deltaStd
                    consecutive_correct = 0
            else:
                consecutive_correct = 0
                noise_std -= deltaStd

            if noise_std <= 1:
                noise_std = 1


    return chosen_letter_array, correct_array, std_array, image2_array, weights


numTrials = 3
block = 1

chosen_letter_array, correct_array, std_array, image2_array, weights = doTrial(numTrials, block, noise_std=1)
print("##################################")
print("First Image:", chosen_letter_array)
print("Second Image:", image2_array)
print("Correct responses:", correct_array)
print("Standard deviation by trial:", std_array)
print("Weights by trial:", weights)
print("##################################")
core.quit()

a = event.waitKeys(keyList=abortKey)
