from psychopy import core, visual, sound, event, clock
import numpy as np
from numpy import random
import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as elib
import serial

# random
seed = 1234
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
dotInterval = 0.5 #seconds
potInterval = 0.1 #seconds
line_top = -150
line_bottom = -200
barX = 75
barY = -150
barWidth = 10
alpha = 1 #loss/win
use_elib = False

# elib setup
if(use_elib):
    elib.setRefreshRate(refreshRate)
    expName="ev3"
    dbConf=elib.data5
    [pid,sid,fname]=elib.startExp(expName,dbConf,pool=1,lockBox=True,refreshRate=refreshRate)    
    froot=fname[:-4]
    resp_file=open(froot+".resp", "w")
    stim_file=open(froot+".stim", "w")
    summary_file=open(froot+".summary", "w")
else:  
    resp_file = open("test_resp", "w")
    stim_file=open("test_stim", "w")
    summary_file=open("test_summary", "w")


# serial setup
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)
ser.reset_input_buffer()

# window
win = visual.Window(units="pix", size=(500, 500), color=[-1, -1, -1], fullscr=True)
screen_width = win.size[0]

# axes
xAxis = visual.Line(win, start=(-1000, 0), end=(1000, 0), lineColor=[255, 0, 0], lineWidth=0.5)
yAxis = visual.Line(win, start=(0, 1000), end=(0, 0), lineColor=[255, 0, 0], lineWidth=0.5)
mid_line = (line_top + line_bottom) / 2

# line objects
top_line = visual.Line(win, start=(0, mid_line), end=(0, mid_line), lineColor="green", lineWidth=5)
bottom_line = visual.Line(win, start=(0, mid_line), end=(0, mid_line), lineColor="green", lineWidth=5)
mid_line = (line_top + line_bottom) / 2

top_left_bar = visual.Rect(win, pos = (-barX, barY), fillColor = 'green', width = barWidth+1, height = 0, anchor = 'bottom')
top_right_bar = visual.Rect(win, pos = (barX, barY), fillColor = 'green', width = barWidth+1, height = 0, anchor = 'bottom')
bottom_left_bar = visual.Rect(win, pos = (-barX,barY), fillColor = 'red', width = barWidth, height = 0, anchor = 'top')
bottom_right_bar = visual.Rect(win, pos = (barX,barY), fillColor = 'red', width = barWidth, height = 0, anchor = 'top')

# outline def
visual_limit = 250
bottom_max = visual_limit / 2
top_max = bottom_max * alpha
total_outline_height = bottom_max + top_max
outline_center_y = barY + (top_max - bottom_max) / 2

outline_left = visual.Rect(
    win, pos=(-barX, outline_center_y), fillColor=None, lineColor='grey',
    width=barWidth + 5, lineWidth=2.5, height=total_outline_height, anchor='center'
)

outline_right = visual.Rect(
    win, pos=(barX, outline_center_y), fillColor=None, lineColor='grey',
    width=barWidth + 5, lineWidth=2.5, height=total_outline_height, anchor='center'
)


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

# feedback setup
last_feedback_text = None
last_feedback_color = 'white'
total_score = 0

def showBlockStartScreen(text):
    message = visual.TextStim(win, text=text, height=30, color='white', pos=(0, 0))
    instruction = visual.TextStim(win, text="Press any key to start", height=20, color='white', pos=(0, -40))
    while True:
        message.draw()
        instruction.draw()
        win.flip()
        keys = event.getKeys()
        if keys:
            if 'escape' in keys:
                core.quit()
            break

def displayDots(mu, sd, endChance, dotY, dotRadius, dotInterval, numTrials):
    global last_feedback_text, last_feedback_color, total_score

    resp = []
    stim = []
    summary = []

    inside_threshold = 25
    max_offset = screen_width / 2 - 50
    visual_limit = 250

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

            # visual feedback
            top_line.start = (x_offset, mid_line)
            top_line.end = (x_offset, line_top)
            bottom_line.start = (x_offset, mid_line)
            bottom_line.end = (x_offset, line_bottom)

            if(x_offset >= 0):
                top_right_bar.height = x_offset/2*alpha
                bottom_right_bar.height = x_offset/2
                top_left_bar.height = 0
                bottom_left_bar.height = 0
            else:
                top_left_bar.height = -x_offset/2*alpha
                bottom_left_bar.height = -x_offset/2
                top_right_bar.height = 0
                bottom_right_bar.height = 0

            if abs(x_offset) <= inside_threshold:
                top_line.lineColor = 'green'
                bottom_line.lineColor = 'green'
                outline_right.lineColor = 'green'
                outline_left.lineColor = 'green'
            else:
                top_line.lineColor = 'red'
                bottom_line.lineColor = 'red'
                outline_right.lineColor = 'red'
                outline_left.lineColor = 'red'

            # end inside threshold edge case
            if not moved_outside:
                if abs(x_offset) > inside_threshold:
                    moved_outside = True
            else:
                if abs(x_offset) <= inside_threshold:
                    break

        reset_text = visual.TextStim(win, text="Please move the knob outside the green zone, then back inside to start.", height=25, color='white', pos=(0, 0))
        reset_text.draw()

        top_line.draw()
        bottom_line.draw()
        #top_left_bar.draw()
        #top_right_bar.draw()
        #bottom_left_bar.draw()
        #bottom_right_bar.draw()
        #outline_left.draw()
        #outline_right.draw()
        win.flip()

    trial = 0
    trial_score = None
    while(trial < numTrials):
        dotNum = 0

        correct = -1 if rng.integers(0, 2) == 0 else 1
        coordinates = np.round(rng.normal(mu * correct, sd, 20))
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
                norm_val = -(val - 512) / 512.0
                x_offset = norm_val * max_offset

                # +- 250 pixel clamp
                x_offset = max(-visual_limit, min(visual_limit, x_offset))

                top_line.start = (x_offset, mid_line)
                top_line.end = (x_offset, line_top)
                bottom_line.start = (x_offset, mid_line)
                bottom_line.end = (x_offset, line_bottom)

                if(x_offset >= 0):
                    top_right_bar.height = x_offset/2*alpha
                    bottom_right_bar.height = x_offset/2
                    top_left_bar.height = 0
                    bottom_left_bar.height = 0
                else:
                    top_left_bar.height = -x_offset/2*alpha
                    bottom_left_bar.height = -x_offset/2
                    top_right_bar.height = 0
                    bottom_right_bar.height = 0

                #feedback
                if abs(x_offset) <= inside_threshold:
                    top_line.lineColor = 'green'
                    bottom_line.lineColor = 'green'
                    outline_right.lineColor = 'green'
                    outline_left.lineColor = 'green'
                else:
                    top_line.lineColor = 'red'
                    bottom_line.lineColor = 'red'
                    outline_right.lineColor = 'red'
                    outline_left.lineCclor = 'red'

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
            
            # ready phase draw
            ready_text = visual.TextStim(win, text="Ready? Move the knob to the middle to continue.", height=30, color='white', pos=(0, 0))
            ready_text.draw()
            top_line.draw()
            bottom_line.draw()
            #top_left_bar.draw()
            #top_right_bar.draw()
            #bottom_left_bar.draw()
            #bottom_right_bar.draw()
            #outline_left.draw()
            #outline_right.draw()
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
        frame_in_trial = 0
        outline_right.lineColor = 'grey'
        outline_left.lineColor = 'grey'

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
                norm_val = -(val - 512) / 512.0
                x_offset = norm_val * max_offset
                x_offset = max(-visual_limit, min(visual_limit, x_offset))

                top_line.start = (x_offset, mid_line)
                top_line.end = (x_offset, mid_line + abs(x_offset)/5)
                bottom_line.start = (x_offset, mid_line)
                bottom_line.end = (x_offset, mid_line - abs(x_offset)/2)

                if(x_offset >= 0):
                    top_right_bar.height = x_offset/2*alpha
                    bottom_right_bar.height = x_offset/2
                    top_left_bar.height = 0
                    bottom_left_bar.height = 0
                else:
                    top_left_bar.height = -x_offset/2*alpha
                    bottom_left_bar.height = -x_offset/2
                    top_right_bar.height = 0
                    bottom_right_bar.height = 0

                top_line.lineColor = 'green'
                bottom_line.lineColor = 'red'

            # update pot reading every potInterval seconds
            if frame_in_trial % (potInterval*refreshRate) == 0:
                resp.append([trial, frame_in_trial/refreshRate, x_offset])

            # update dots every dotInterval seconds
            if frame_in_trial % (dotInterval*refreshRate) == 0:
                dotNum += 1
                if dotNum >= len(coordinates):
                    dotNum = 0
                circ.pos = (coordinates[dotNum], dotY)
                stim.append([trial, frame_in_trial/refreshRate, coordinates[dotNum]])
                if dotNum > 3:
                    if ((rng.random() < endChance) or dotNum > 9):
                        final_side = np.sign(x_offset)
                        # end in middle edge case
                        if final_side == 0:
                            final_side = 1

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
                        summary.append([trial, dotNum, correct, x_offset, int(trial_score)])
                        trial += 1

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

                                if(x_offset >= 0):
                                    top_right_bar.height = x_offset/2*alpha
                                    bottom_right_bar.height = x_offset/2
                                    top_left_bar.height = 0
                                    bottom_left_bar.height = 0
                                else:
                                    top_left_bar.height = -x_offset/2*alpha
                                    bottom_left_bar.height = -x_offset/2
                                    top_right_bar.height = 0
                                    bottom_right_bar.height = 0

                                if abs(x_offset) <= inside_threshold:
                                    top_line.lineColor = 'green'
                                    bottom_line.lineColor = 'green'
                                    outline_right.lineColor = 'green'
                                    outline_left.lineColor = 'green'
                                else:
                                    top_line.lineColor = 'red'
                                    bottom_line.lineColor = 'red'
                                    outline_right.lineColor = 'red'
                                    outline_left.lineColor = 'red'

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
                            #top_left_bar.draw()
                            #top_right_bar.draw()
                            #bottom_left_bar.draw()
                            #bottom_right_bar.draw()
                            #outline_left.draw()
                            #outline_right.draw()
                            win.flip()

                        break

            circ.draw()
            xAxis.draw()
            yAxis.draw()
            #top_line.draw()
            #bottom_line.draw()
            top_left_bar.draw()
            top_right_bar.draw()
            bottom_left_bar.draw()
            bottom_right_bar.draw()
            outline_left.draw()
            outline_right.draw()
            win.flip()

            frame_in_trial += 1

    return resp, stim, summary

# main
endChance = 0.15
numTrials = 10
total_score = 0
showBlockStartScreen("Tutorial Block")
resp, stim, summary = displayDots(mu, sd, endChance, dotY, dotRadius, dotInterval, numTrials)
numTrials = 50
total_score = 0
showBlockStartScreen("Main Block")
resp, stim, summary = displayDots(mu, sd, endChance, dotY, dotRadius, dotInterval, numTrials)

# data writing
resp_file.write("trial\ttime\tpot_val\n")
for row in resp:
    resp_file.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

stim_file.write("trial\ttime\tstim_coord\n")
for row in stim:
    stim_file.write(f"{row[0]}\t{row[1]}\t{row[2]}\n")

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

hz=round(win.getActualFrameRate())
[resX,resY]=win.size
if(use_elib):
    elib.stopExp(sid,hz,resX,resY,seed,dbConf)
win.close()
ser.close()
core.quit()
