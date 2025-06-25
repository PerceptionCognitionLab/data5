from psychopy import visual, event, core, prefs, sound 
import sys
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from numpy.fft import fft2, ifft2, fftshift, ifftshift
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as exlib

prefs.hardware['audioLib']=['PTB']
prefs.hardware['audioLatencyMode']=3

# region
refreshRate=165
exlib.setRefreshRate(refreshRate)
trialClock=core.Clock()
expName="mp1"
dbConf=exlib.data5
seed = random.randrange(1e6)
# [pid,sid,fname]=exlib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)
[pid,sid,fname] = [1,1,'Me.dat']
fptr = open(fname,'w')
# endregion

correctSound1=sound.Sound(value=600,secs=0.1)
correctSound2=sound.Sound(value=800,secs=0.1)
errorSound=sound.Sound(value=500,secs=0.2)

# Parameters
letters = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
noises = ['#', '@', '$', '%', '&']
soa = 20
soa_practice = [20, 24, 28]
step_size = 1
n_trials = 50
n_practices = 10
correct_counter = 0
data = []
FixationFrame = 80
NosieFrame = 8

# Letter Stimulus 
def ShowImage(image):
    plt.imshow(image, cmap='gray', vmin=0, vmax=1)
    plt.axis('off') 
    plt.show()

def LetterImage(letter, image_size = 128, letter_size = 64, bg_color = 0, letter_color = 1):
    image = Image.new('L', (image_size, image_size), color=bg_color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", letter_size)
    bbox = draw.textbbox((0, 0), letter, font = font)
    letter_w, letter_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    image_w, image_h = image.size
    x = (image_w - letter_w) // 2 - bbox[0]
    y = (image_h - letter_h) // 2 - bbox[1]
    draw.text((x, y), letter, font = font, fill=letter_color)
    return np.array(image).astype(np.float32)


def Norm(image):
    return 2 * image - 1

# Visual Setup
win = visual.Window(size=(1920, 1080), color=-1, units="pix", fullscr=True)
stim = visual.ImageStim(win, size=(512, 512), units="pix")

# Welcome Screen
text = visual.TextStim(win, text="Welcome to the experiment! Press SPACE to begin the instruction", color=1.0, height=24)
text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Instruction Screen
text = visual.TextStim(win, text="In this experiment, you will see a letter embedded in noise. The letter will be chosen from the second row of the keyboard - [A,S,D,F,G,H,J,K,L]\
                                        The below one is a letter A.\
                                        \n\n The letter will be briefly flashed and then immediately masked by some other symbols, your task is to choose the letter you see using the second row of the keyboard.\
                                        \n\n Press SPACE to continue", color=1.0, height=24, pos = (0, 300))
text.draw()
image = visual.ImageStim(image = np.flipud(Norm(LetterImage(letter = 'A'))), win = win, size=(512, 512), pos = (0, -200), units="pix")
image.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Practice trail screen
text = visual.TextStim(win, text="We will begin with several practice trials, feedback on correctness will be provided after each trial.\
                                \n\n Choose the letter using the second row of the keyboard.\
                                \n\n Press SPACE to start the practice trials. ", color=1.0, height=24)
text.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Trial Loop
for trial in range(n_practices):
    if 'escape' in event.getKeys():
        print("Experiment aborted by user.")
        break

    # Fixation
    fixation = visual.TextStim(win, text="+", color=1.0, height=48)

    # Stimulus
    letter, practice_soa = random.choice(letters), random.choice(soa_practice)
    stim.image = np.flipud(Norm(LetterImage(letter)))

    # Noise
    noises = random.sample(noises, 3)
    noise0 = visual.ImageStim(win, size=(512, 512), units="pix", image = np.flipud(Norm(LetterImage(noises[0]))))
    noise1 = visual.ImageStim(win, size=(512, 512), units="pix", image = np.flipud(Norm(LetterImage(noises[1]))))
    noise2 = visual.ImageStim(win, size=(512, 512), units="pix", image = np.flipud(Norm(LetterImage(noises[2]))))

    # RunFrame
    frames = [fixation, stim, noise0, noise1, noise2]
    frameDurations = [FixationFrame, practice_soa, NosieFrame, NosieFrame, NosieFrame] 
    stamps = exlib.runFrames(win, frames, frameDurations, trialClock)

    # Decision
    wait = visual.TextStim(win, text="Choose the letter", color=1.0, height=48)
    wait.draw()
    win.flip()
    keys = event.waitKeys(keyList=['a', 's', 'd','f','g','h','j','k','l','escape'])
    if 'escape' in keys:
        print("Experiment aborted by user.")
        break
    win.flip()
    response = keys[0].upper()
    correct = response == letter

    # Feedback 
    if correct:
        feedback_text = "Correct!"
        feedback_color = 'green'
        feedback = visual.TextStim(win, text=feedback_text, color=feedback_color, height=36)
        feedback.draw()
        win.flip()
        correctSound1.play()
        core.wait(0.1)
        correctSound2.play() 
        core.wait(0.4) 
    else:
        feedback_text = f"Wrong! The correct letter was: {letter}"
        feedback_color = 'red'
        feedback = visual.TextStim(win, text=feedback_text, color=feedback_color, height=36)
        feedback.draw()
        win.flip()
        errorSound.play()
        core.wait(0.5)  

    win.flip()
    core.wait(0.5)


# --- Main Staircase Block ---
text = visual.TextStim(win, text="Excellent! Here comes the main experiment. No feedback on correct letter will be given! This time the task is more difficult, please pay attention\
                                \n\n Choose the letter using the second row of the keyboard.\
                                \n\n Press SPACE to start the main experiment. ", color=1.0, height=24)

text.draw()
win.flip()
event.waitKeys(keyList=['space'])

for trial in range(n_trials):
    if 'escape' in event.getKeys():
        print("Experiment aborted by user.")
        break

    # Fixation
    fixation = visual.TextStim(win, text="+", color=1.0, height=48)

    # Stimulus
    letter = random.choice(letters)
    stim.image = np.flipud(Norm(LetterImage(letter)))

    # Noise
    noises = random.sample(noises, 3)
    noise0 = visual.ImageStim(win, size=(512, 512), units="pix", image = np.flipud(Norm(LetterImage(noises[0]))))
    noise1 = visual.ImageStim(win, size=(512, 512), units="pix", image = np.flipud(Norm(LetterImage(noises[1]))))
    noise2 = visual.ImageStim(win, size=(512, 512), units="pix", image = np.flipud(Norm(LetterImage(noises[2]))))

    # RunFrame
    frames = [fixation, stim, noise0, noise1, noise2]
    frameDurations = [FixationFrame,soa, NosieFrame, NosieFrame, NosieFrame] 
    stamps = exlib.runFrames(win, frames, frameDurations, trialClock)

    # Decision
    wait = visual.TextStim(win, text="Choose the letter", color=1.0, height=48)
    wait.draw()
    win.flip()
    keys = event.waitKeys(keyList=['a', 's', 'd','f','g','h','j','k','l','escape'])
    if 'escape' in keys:
        print("Experiment aborted by user.")
        break
    win.flip()
    response = keys[0].upper()
    correct = response == letter

    # Feedback 
    if correct:
        correctSound1.play()
        core.wait(0.1)
        correctSound2.play() 
        core.wait(0.4) 
    else:
        errorSound.play()
        core.wait(0.5)  

    data.append({"trial": trial+1, "letter": letter, "response": response,
                 "correct": correct, "soa": soa})
    if correct:
        correct_counter += 1
        if correct_counter == 2:
            soa = int(max(0, soa - step_size))
            correct_counter = 0
    else:
        soa = int(soa + step_size)
        correct_counter = 0
    core.wait(0.5)

hz=round(win.getActualFrameRate())
[resX,resY]=win.size
# exlib.stopExp(sid,hz,resX,resY,seed,dbConf)

win.close()

df = pd.DataFrame(data)
df.to_csv(f"{pid}_{sid}_TLetter.csv", index=False)

