from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random
import sys
import serial

# random
rng = random.default_rng()
seed = random.randint(1,1000000)
rng = random.default_rng(seed)

# globals
abortKey = ['escape']
refreshRate = 60
expName = "ev3"
mu = 10
sd = 25
numDots = 30
dotY = 0
dotRadius = 5
dotInterval = 0.5
potInterval = 0.1

# data files
[pid, sid] = [1,1]
pot_fptr = open("pot_test.txt", "w")
stim_fptr = open("stim_test.txt", "w")
summary_fptr = open("summary_test.txt", "w")

# serial setup
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.01)
ser.reset_input_buffer()

# window
win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
screen_width = win.size[0]

# axes
xAxis = visual.Line(win, start=(-1000, 0), end=(1000, 0), lineColor=[255, 0, 0], lineWidth=0.5)
yAxis = visual.Line(win, start=(0, 1000), end=(0, 0), lineColor=[255, 0, 0], lineWidth=0.5)

def displayDots(mu, sd, endChance, dotY, dotRadius, dotInterval, numTrials):
    resp = []
    stim = []
    summary = []
    # bars
    bar_left = visual.Rect(win, width=0, height=20, fillColor="green",
                           lineColor="black", pos=(0, -100), anchor='right')
    bar_right = visual.Rect(win, width=0, height=20, fillColor="green",
                            lineColor="black", pos=(0, -100), anchor='left')

    trial = 0
    while(trial < numTrials):
        dotNum = 0

        correct = -1 if rng.integers(0, 2) == 0 else 1
        coordinates = np.round(np.random.normal(mu * correct, sd, 20))
        circ = visual.Circle(win, pos=(coordinates[dotNum], dotY),
                             fillColor=[1, 1, 1], radius=dotRadius)

        inside_threshold  = 25
        inside_time = None

        # ready check
        while True:
            if "escape" in event.getKeys():
                return resp, stim

            # serial
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
                norm_val = (val - 512) / 512.0

                if norm_val >= 0:
                    bar_left.width = norm_val * (screen_width / 2)
                    bar_right.width = 0
                else:
                    bar_right.width = abs(norm_val) * (screen_width / 2)
                    bar_left.width = 0

            # draw
            if (bar_left.width <= 20) and (bar_right.width <= 20):
                bar_left.fillColor = 'green'
                bar_right.fillColor = 'green'
            else:
                bar_left.fillColor = 'red'
                bar_right.fillColor = 'red'
            bar_left.draw()
            bar_right.draw()
            ready_text = visual.TextStim(win, text="Ready? Move the knob to the middle to continue.", height=30, color='white', pos=(0, 0))
            ready_text.draw()
            win.flip()

            # check if bars are inside threshold
            if((bar_left.width <= inside_threshold) & (bar_right.width <= inside_threshold)):
                if inside_time is None:
                    inside_time = core.getTime()
                elapsed = core.getTime() - inside_time
            else:
                inside_time = None
                elapsed = 0
            if(elapsed >= 1):
                break

        # trial dots loop
        trialClock = core.Clock()
        lastPotTime = 0
        lastDotTime = 0
        frame_in_trial = 0

        while True:
            if "escape" in event.getKeys():
                return resp, stim

            currentTime = trialClock.getTime()

            # serial
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
                norm_val = (val - 512) / 512.0

                if norm_val >= 0:
                    bar_left.width = norm_val * (screen_width / 2)
                    bar_right.width = 0
                else:
                    bar_right.width = abs(norm_val) * (screen_width / 2)
                    bar_left.width = 0

            # update pot reading every potInterval seconds
            if currentTime - lastPotTime >= potInterval:
                resp.append([trial, round(currentTime, 2), val])
                lastPotTime = currentTime

            # update dots every dotInterval seconds
            if currentTime - lastDotTime >= dotInterval:
                dotNum += 1
                if dotNum >= len(coordinates):
                    dotNum = 0
                circ.pos = (coordinates[dotNum], dotY)
                stim.append([trial, round(currentTime, 2), coordinates[dotNum]])
                if dotNum >= 3:
                    if np.random.rand() < endChance:
                        summary.append([trial, dotNum, correct, val])
                        trial += 1
                        break
                lastDotTime = currentTime

            circ.draw()
            xAxis.draw()
            yAxis.draw()
            bar_left.draw()
            bar_right.draw()
            win.flip()

            frame_in_trial += 1

    return resp, stim, summary




# main
numTrials = 3
endChance = 0.15
resp, stim, summary = displayDots(mu, sd, endChance, dotY, dotRadius, dotInterval, numTrials)

# data writing
with open("pot_test.txt", "w") as fptr:
    for row in resp:
        fptr.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

with open("stim_test.txt", "w") as stim_file:
    for row in stim:
        stim_file.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

with open("summary_test.txt", "w") as summary_file:
    summary_file.write("trial\tpoints_drawn\tcorrect\tfinal_pot_val\n")
    for row in summary:
        summary_file.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\n")


win.close()
ser.close()
core.quit()
fptr.close()
