from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random
import sys
import serial

# --- Random setup ---
rng = random.default_rng()
seed = random.randint(1,1000000)
rng = random.default_rng(seed)

# --- Globals ---
abortKey = ['9']
refreshRate = 165
expName = "ev2"
[pid, sid, fname] = [1, 1, 'test']
fptr = open(fname, "w")
mu = 10
sd = 25
numDots = 30
dotY = 0
dotRadius = 5
dotInterval = 0.3
clock = core.Clock()

# --- Serial setup for Arduino potentiometer ---
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.01)
ser.reset_input_buffer()

# --- PsychoPy window ---
win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
screen_width = win.size[0]

# Axes
xAxis = visual.Line(win, start=(0, -500), end=(0, 500), lineColor=[255, 0, 0], lineWidth=0.5)
yAxis = visual.Line(win, start=(-1000, 0), end=(1000, 0), lineColor=[255, 0, 0], lineWidth=0.5)

# --- Sounds (optional) ---
# correctSound1 = sound.Sound(500, secs=0.25)
# correctSound2 = sound.Sound(1000, secs=0.25)
# incorrectSound1 = sound.Sound(500, secs=0.5)
# incorrectSound2 = sound.Sound(375, secs=0.5)

def playCorrectSound():
    correctSound1.play()
    core.wait(0.25)
    correctSound2.play()
    core.wait(0.25)

def playIncorrectSound():
    incorrectSound1.play()
    incorrectSound2.play()
    core.wait(0.5)

def ready():
    visual.TextStim(win, text="Ready? Press any key to continue.", height=30, color='white').draw()
    win.flip()
    while True:
        if event.getKeys(abortKey):
            win.close(); ser.close(); core.quit()
        if event.getKeys():
            break

def countdown():
    win.flip(); core.wait(0.5)
    for color in ([255,0,0],[255,255,0],[0,255,0]):
        marker = visual.Circle(win, pos=(0,0), fillColor=color, radius=5)
        marker.draw(); xAxis.draw(); yAxis.draw()
        win.flip(); core.wait(0.5)
    core.wait(np.random.normal(0.5, 0.1) + np.random.normal(0,0.1))

def manualTutorial():
    ready()
    coordinates = [10,87,44,-49,-10,-71,-31,18,13,-37,42,-97,-70,-88]
    for i in range(len(coordinates)):
        if i in [0,3,6]:
            countdown()
        circ = visual.Circle(win, pos=(coordinates[i], dotY), fillColor=[1,1,1], radius=dotRadius)
        circ.draw(); xAxis.draw(); yAxis.draw()
        win.flip()
        event.clearEvents()
        while True:
            if event.getKeys(abortKey):
                win.close(); ser.close(); core.quit()
            if i == 2 and event.getKeys('m'):
                playCorrectSound(); break
            elif i in [5,13] and event.getKeys('x'):
                playCorrectSound(); break
            elif event.getKeys('space'):
                break

def autoTutorial(trial, interval):
    coordinates = [np.round(np.random.normal(mu*trial, sd)) for _ in range(numDots)]
    for coord in coordinates:
        event.clearEvents()
        circ = visual.Circle(win, pos=(coord, dotY), fillColor=[1,1,1], radius=dotRadius)
        for _ in range(round(refreshRate * interval)):
            responseTime = round(clock.getTime(), 3)
            if event.getKeys(abortKey):
                win.close(); ser.close(); core.quit()
            if event.getKeys(['x']):
                playCorrectSound() if trial == -1 else playIncorrectSound()
                return
            if event.getKeys(['m']):
                playCorrectSound() if trial == 1 else playIncorrectSound()
                return
            circ.draw(); xAxis.draw(); yAxis.draw()
            win.flip()
    playIncorrectSound()

def displayDots(mu, sd, exponent, dotY, dotRadius, dotInterval, numTrials):
    trial = 0
    frameNum = 0
    dotNum = 0
    endChance = 0
    resp = []

    correct = -1 if rng.integers(0,2) == 0 else 1
    coordinates = [np.round(np.random.normal(mu*correct, sd)) for _ in range(numDots)]
    circ = visual.Circle(win, pos=(coordinates[dotNum], dotY), fillColor=[1,1,1], radius=dotRadius)

    # Bars
    bar_left = visual.Rect(win, width=0, height=20, fillColor="green",
                           lineColor="black", pos=(0, -200), anchor='right')
    bar_right = visual.Rect(win, width=0, height=20, fillColor="green",
                            lineColor="black", pos=(0, -200), anchor='left')

    print("Starting displayDots")  # debug

    while trial < numTrials:
        if "escape" in event.getKeys():
            break

        # --- Read potentiometer (fixed) ---
        line = None
        while ser.in_waiting:
            try:
                raw = ser.readline().decode("utf-8", errors="ignore").strip()
                if raw:
                    line = raw
            except Exception:
                continue

        if line and line.isdigit():
            val = int(line)
            norm_val = (val - 512) / 512.0  # -1 → +1

            if norm_val >= 0:
                bar_right.width = norm_val * (screen_width / 2)
                bar_left.width = 0
            else:
                bar_left.width = abs(norm_val) * (screen_width / 2)
                bar_right.width = 0

        # --- Dot logic ---
        if frameNum >= round(refreshRate * dotInterval):
            dotNum += 1
            if dotNum >= len(coordinates):
                dotNum = 0
            circ.pos = (coordinates[dotNum], dotY)

            if dotNum == 3:
                endChance = exponent
            endChance = endChance * (exponent + 1)
            if np.random.normal(0, 1) <= endChance and line is not None:
                resp.append(val)  # append potentiometer value
                dotNum = 0
                endChance = 0
                trial += 1

            frameNum = 0  # reset counter

        # --- Draw everything ---
        circ.draw()
        xAxis.draw()
        yAxis.draw()
        bar_left.draw()
        bar_right.draw()

        win.flip()
        frameNum += 1

    return resp

# --- Run experiment ---
numTrials = 3
exponent = 0.25
print(displayDots(mu, sd, exponent, dotY, dotRadius, dotInterval, numTrials))

win.close()
ser.close()
core.quit()
fptr.close()
