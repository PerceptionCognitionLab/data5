from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random
import sys
import serial

# random
rng = random.default_rng()
seed = random.randint(1, 1000000)
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
line_top = -150
line_bottom = -200

# data files
[pid, sid] = [1, 1]

# serial setup
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)
ser.reset_input_buffer()

# window
win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
screen_width = win.size[0]

# axes
xAxis = visual.Line(win, start=(-1000, 0), end=(1000, 0), lineColor=[255, 0, 0], lineWidth=0.5)
yAxis = visual.Line(win, start=(0, 1000), end=(0, 0), lineColor=[255, 0, 0], lineWidth=0.5)

# mid point for zero height baseline
mid_line = (line_top + line_bottom) / 2

# create line objects for top and bottom parts
top_line = visual.Line(win, start=(0, mid_line), end=(0, mid_line), lineColor="green", lineWidth=5)
bottom_line = visual.Line(win, start=(0, mid_line), end=(0, mid_line), lineColor="green", lineWidth=5)

# sounds
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
    incorrectSound2.play()
    core.wait(0.5)

# Globals to store feedback for next trial ready phase
last_feedback_text = None
last_feedback_color = 'white'
total_score = 0  # keep total score global for reference

def displayDots(mu, sd, endChance, dotY, dotRadius, dotInterval, numTrials):
    global last_feedback_text, last_feedback_color, total_score

    resp = []
    stim = []
    summary = []

    inside_threshold = 25  # pixel threshold from center
    max_offset = screen_width / 2 - 50  # max line movement from center
    visual_limit = 250  # visual clamp in pixels

    # === Added: initial knob reset phase before trials ===
    moved_outside = False
    while True:
        if "escape" in event.getKeys():
            return resp, stim, summary

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
            norm_val = -(val - 512) / 512.0
            x_offset = norm_val * max_offset
            x_offset = max(-visual_limit, min(visual_limit, x_offset))

            # Draw lines for visual feedback
            top_line.start = (x_offset, mid_line)
            top_line.end = (x_offset, line_top)
            bottom_line.start = (x_offset, mid_line)
            bottom_line.end = (x_offset, line_bottom)

            if abs(x_offset) <= inside_threshold:
                top_line.lineColor = 'green'
                bottom_line.lineColor = 'green'
            else:
                top_line.lineColor = 'red'
                bottom_line.lineColor = 'red'

            # Reset logic: first outside then back inside
            if not moved_outside:
                if abs(x_offset) > inside_threshold:
                    moved_outside = True
            else:
                if abs(x_offset) <= inside_threshold:
                    break  # Ready to start experiment

        reset_text = visual.TextStim(win, text="Please move the knob outside the green zone, then back inside to start.", height=25, color='white', pos=(0, 0))
        reset_text.draw()

        top_line.draw()
        bottom_line.draw()
        win.flip()
    # === End initial knob reset phase ===

    trial = 0
    trial_score = None  # Initialize trial_score here to avoid reference errors
    while(trial < numTrials):
        dotNum = 0

        correct = -1 if rng.integers(0, 2) == 0 else 1
        coordinates = np.round(np.random.normal(mu * correct, sd, 20))
        circ = visual.Circle(win, pos=(coordinates[dotNum], dotY),
                             fillColor=[1, 1, 1], radius=dotRadius)

        inside_time = None

        # ready check before trial
        while True:
            if "escape" in event.getKeys():
                return resp, stim, summary

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
                norm_val = -norm_val  # reverse the knob input
                x_offset = norm_val * max_offset

                # Clamp to ±250 pixels for visual limit
                x_offset = max(-visual_limit, min(visual_limit, x_offset))

                # Set line positions
                top_line.start = (x_offset, mid_line)
                top_line.end = (x_offset, line_top)

                bottom_line.start = (x_offset, mid_line)
                bottom_line.end = (x_offset, line_bottom)

                # Color feedback during ready phase
                if abs(x_offset) <= inside_threshold:
                    top_line.lineColor = 'green'
                    bottom_line.lineColor = 'green'
                else:
                    top_line.lineColor = 'red'
                    bottom_line.lineColor = 'red'

            # draw last feedback if exists, above ready text
            if last_feedback_text:
                feedback_stim = visual.TextStim(win, text=last_feedback_text, height=30, color=last_feedback_color, pos=(0, 110))
                feedback_stim.draw()

                trial_score_val = int(trial_score) if trial_score is not None else 0
                trial_score_stim = visual.TextStim(win, text=f"Trial score: {trial_score_val}", height=30, color=last_feedback_color, pos=(0, 80))
                trial_score_stim.draw()

                score_stim = visual.TextStim(win, text=f"Total score: {int(total_score)}", height=30, color=last_feedback_color, pos=(0, 50))
                score_stim.draw()

                progress_percent = int((trial / numTrials) * 100)
                progress_text = visual.TextStim(win, text=f"Progress: {progress_percent}%", height=15, color='white', pos=(0, 500))
                progress_text.draw()

            # draw ready text
            ready_text = visual.TextStim(win, text="Ready? Move the knob to the middle to continue.", height=30, color='white', pos=(0, 0))
            ready_text.draw()

            top_line.draw()
            bottom_line.draw()
            win.flip()

            # check if line is centered
            if abs(x_offset) <= inside_threshold:
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
                return resp, stim, summary

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
                norm_val = -(val - 512) / 512.0
                x_offset = norm_val * max_offset
                x_offset = max(-visual_limit, min(visual_limit, x_offset))

                top_line.start = (x_offset, mid_line)
                top_line.end = (x_offset, mid_line + abs(x_offset)/5)
                bottom_line.start = (x_offset, mid_line)
                bottom_line.end = (x_offset, mid_line - abs(x_offset)/2)

                top_line.lineColor = 'green'
                bottom_line.lineColor = 'red'

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
                        final_side = np.sign(x_offset)
                        if final_side == 0:
                            final_side = 1  # treat center as right

                        # feedback
                        if final_side == correct:
                            last_feedback_text = "Correct!"
                            playCorrectSound()
                            last_feedback_color = 'green'
                            trial_score = abs(top_line.end[1] - top_line.start[1])
                        else:
                            last_feedback_text = "Incorrect"
                            playIncorrectSound()
                            last_feedback_color = 'red'
                            trial_score = -abs(bottom_line.end[1] - bottom_line.start[1])

                        total_score += trial_score
                        summary.append([trial, dotNum, correct, val, int(trial_score)])

                        trial += 1

                        # === Post-trial knob reset phase with updated text positions ===
                        moved_outside = False
                        while True:
                            if "escape" in event.getKeys():
                                return resp, stim, summary

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
                                norm_val = -(val - 512) / 512.0
                                x_offset = norm_val * max_offset
                                x_offset = max(-visual_limit, min(visual_limit, x_offset))

                                top_line.start = (x_offset, mid_line)
                                top_line.end = (x_offset, line_top)
                                bottom_line.start = (x_offset, mid_line)
                                bottom_line.end = (x_offset, line_bottom)

                                if abs(x_offset) <= inside_threshold:
                                    top_line.lineColor = 'green'
                                    bottom_line.lineColor = 'green'
                                else:
                                    top_line.lineColor = 'red'
                                    bottom_line.lineColor = 'red'

                                if not moved_outside:
                                    if abs(x_offset) > inside_threshold:
                                        moved_outside = True
                                else:
                                    if abs(x_offset) <= inside_threshold:
                                        break

                            if last_feedback_text:
                                feedback_stim = visual.TextStim(win, text=last_feedback_text, height=30, color=last_feedback_color, pos=(0, 110))
                                feedback_stim.draw()

                                trial_score_stim = visual.TextStim(win, text=f"Trial score: {int(trial_score)}", height=30, color=last_feedback_color, pos=(0, 80))
                                trial_score_stim.draw()

                                score_stim = visual.TextStim(win, text=f"Total score: {int(total_score)}", height=30, color=last_feedback_color, pos=(0, 50))
                                score_stim.draw()

                                progress_percent = int((trial / numTrials) * 100)
                                progress_text = visual.TextStim(win, text=f"Progress: {progress_percent}%", height=15, color='white', pos=(0, 500))
                                progress_text.draw()


                            reset_text = visual.TextStim(win, text="Please move the knob outside the green zone, then back inside to continue.", height=25, color='white', pos=(0, 0))
                            reset_text.draw()

                            top_line.draw()
                            bottom_line.draw()
                            win.flip()

                        break
                lastDotTime = currentTime

            circ.draw()
            xAxis.draw()
            yAxis.draw()
            top_line.draw()
            bottom_line.draw()
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
    summary_file.write("trial\tpoints_drawn\tcorrect\tfinal_pot_val\ttrial_score\n")
    for row in summary:
        summary_file.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\n")

# final screen
final_score_text = visual.TextStim(win, text=f"Final Total Score:\n{int(total_score)}", height=30, color='white', pos=(0, 40))
exit_text = visual.TextStim(win, text="Press ESCAPE to exit", height=30, color='white', pos=(0, -40))

while True:
    final_score_text.draw()
    exit_text.draw()
    win.flip()

    if 'escape' in event.getKeys():
        break

win.close()
ser.close()
core.quit()
