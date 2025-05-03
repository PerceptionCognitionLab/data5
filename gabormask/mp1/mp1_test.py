import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import random
from psychopy import visual, core, event, monitors
import numpy as np
import expLib51 as exlib

def get_input(prompt, default):
    try:
        val = input(f"{prompt} (default: {default}): ").strip()
        return type(default)(val) if val else default
    except:
        return default

while True:
    # === Parameter Configuration ===
    print("\n==== Debug Masking Experiment Setup ====")
    prime_ori_abs = get_input("Prime orientation", 45)
    mask_ori_abs = get_input("Mask orientation ", 45)
    prime_sf = get_input("Prime spatial frequency", 1.2)
    mask_sf = get_input("Mask spatial frequency", 1.2)
    prime_contrast = get_input("Prime contrast", 0.05)
    mask_contrast = get_input("Mask contrast", 0.05)

    
    prime_frame= get_input("prime frames", 1)
    SOA_frame = get_input("SOA frames", 0)
    mask_frame = get_input("Mask frames", 7)

    repetition = get_input("Number of trials per condition", 10)
    test_type = get_input("Test type\n1.Try experiment\n2.View congruent\n3.View incongruent", 1)

    # === Housekeeping ===
    refreshRate = 165
    exlib.setRefreshRate(refreshRate)
    trialClock = core.Clock()

    # === Monitor and Window ===
    monitor = monitors.Monitor("MyMonitor")
    monitor.setSizePix((1920, 1080))
    monitor.setWidth(53.1)
    monitor.setDistance(100)
    monitor.saveMon()

    prime_size = 2
    mask_size = 4
    fixation_frame = 120

    bg_color = [0, 0, 0]
    text_color = [-1, -1, -1]
    win_size = (1920, 1080)

    win = visual.Window(units="deg", monitor=monitor, size=win_size, color=bg_color, fullscr=True)

    # === Stimulus Templates ===
    prime = visual.GratingStim(win=win, tex="sin", size=prime_size, sf=prime_sf,
                               contrast=prime_contrast, mask="circle")

    mask_outer = visual.GratingStim(win=win, tex="sin", size = mask_size, sf=mask_sf,
                                    contrast=mask_contrast, mask="circle")

    mask_inner = visual.Circle(win=win, radius=prime_size/2 , fillColor=bg_color, lineColor=bg_color)
    blank = visual.TextStim(win=win, text="", color=text_color, bold=True)
    feedback = visual.TextStim(win=win, text="", color=text_color)

    # === Trial Definitions ===
    trials = []
    if test_type == 1:
        for _ in range(repetition):
            side = random.choice(["left", "right"])
            trials.append(("congruent", side, side))
        for _ in range(repetition):
            prime_side = random.choice(["left", "right"])
            mask_side = "right" if prime_side == "left" else "left"
            trials.append(("incongruent", prime_side, mask_side))
        for _ in range(repetition):
            mask_side = random.choice(["left", "right"])
            trials.append(("neutral", 'NA', mask_side))
    if test_type == 2:
        for _ in range(repetition):
            side = random.choice(["left", "right"])
            trials.append(("congruent", side, side))
    if test_type == 3:
        for _ in range(repetition):
            prime_side = random.choice(["left", "right"])
            mask_side = "right" if prime_side == "left" else "left"
            trials.append(("incongruent", prime_side, mask_side))

    random.shuffle(trials)

    correct_con = 0
    correct_inc = 0
    correct_neu = 0

    for trial_type, prime_dir, mask_dir in trials:
        if prime_dir == 'NA':
            mask_ori = -mask_ori_abs if mask_dir == "left" else mask_ori_abs
            mask_outer.ori = mask_ori
            mask = visual.BufferImageStim(win=win, stim=[mask_outer, mask_inner])
            frames = [blank, mask]
            frameDurations = [fixation_frame+SOA_frame, mask_frame]  
        else:
            prime_ori = -prime_ori_abs if prime_dir == "left" else prime_ori_abs
            mask_ori = -mask_ori_abs if mask_dir == "left" else mask_ori_abs

            prime.ori = prime_ori
            mask_outer.ori = mask_ori
            mask = visual.BufferImageStim(win=win, stim=[mask_outer, mask_inner])
            mask_prime = visual.BufferImageStim(win=win, stim=[mask_outer, mask_inner, prime])

            # === Trial Sequence ===
            if SOA_frame != 0:
                frames = [blank, prime, mask_prime, mask]
                frameDurations = [fixation_frame, SOA_frame, prime_frame-SOA_frame, mask_frame-(prime_frame-SOA_frame)]
            else:
                frames = [blank, mask_prime, mask]
                frameDurations = [fixation_frame, prime_frame, mask_frame-prime_frame]  

        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)
        if test_type == 1:
            keys = event.waitKeys(keyList=["x", "m", "escape"])
            if "escape" in keys:
                win.close()
                core.quit()
            response = "no" if keys[0] == "x" else "yes"
            if prime_dir != 'NA':
                correct_response = 'yes'
            else:
                correct_response = 'no'
    
            is_correct = response == correct_response 
            '''
            feedback.text = "Correct!" if is_correct else "Wrong"
            feedback.color = text_color if is_correct else text_color
            feedback.draw()
            win.flip()
            '''
            core.wait(0.5)

            if trial_type == "congruent":
                correct_con += is_correct
            if trial_type == "incongruent":
                correct_inc += is_correct
            if trial_type == "neutral":
                correct_neu += is_correct

    if test_type == 1:
    # === Results ===
        acc_con = correct_con / repetition * 100
        acc_inc = correct_inc / repetition * 100
        acc_neu = correct_neu / repetition * 100

        result_text = visual.TextStim(win, text=f"Accuracy:\nCongruent: {acc_con:.1f}%\nIncongruent: {acc_inc:.1f}%\nNeutral: {acc_neu:.1f}%\n\nPress space to exit",
                                    height=1, color=text_color)
        result_text.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

    # === Restart or Exit ===
    win.close()
    again = input("Restart with new settings? (y/n): ").strip().lower()
    if again != "y":
        break

core.quit()
