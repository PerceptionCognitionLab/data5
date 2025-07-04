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

    prime_ori_abs = 45
    mask_ori_abs = 45
    prime_sf = 1.2
    mask_sf = 1.2
    prime_contrast = 0.05
    mask_contrast = 0.05
    prime_phase = 0
    mask_phase = 0
    prime_frame = 1
    mask_frame = 7
    SOA_frame = 0

    repetition = 10
    test_type = 1
    prime_type = 1 # 1 wihout edge, 2 with edge

    option = get_input("Change settings?\n1.No change\n2.Change orientaion\n3.Change spatial frequency\n4.Change contrast\n5.Change phase\n6.Chnage SOA frames\n7.Change prime type\n8.Change test type", 1)
    # === Parameter Configuration ===
    while option != 1:
        if option == 2:
            prime_ori_abs = get_input("Prime orientation", 45)
            # mask_ori_abs = get_input("Mask orientation ", 45)
        if option == 3:
            prime_sf = get_input("Prime spatial frequency", 1.2)
            mask_sf = get_input("Mask spatial frequency", 1.2)
        if option == 4:
            prime_contrast = get_input("Prime contrast", 0.05)
            # mask_contrast = get_input("Mask contrast", 0.05)
        if option == 5:
            prime_phase = get_input("Prime phase", 0)
            # mask_phase = get_input("Mask phase", 0)
        if option == 6:
            SOA_frame = get_input("SOA frames", 0)
            # mask_frame = get_input("Mask frames", 7)
        if option == 7:
            prime_type = get_input("prime type\n1.Without edge\n2.With edge", 1)
        if option == 8:
            test_type = get_input("Test type\n1.Try experiment\n2.View congruent\n3.View incongruent", 1)
            break
        option = get_input("Change other settings?\n1.No change\n2.Change orientaion\n3.Change spatial frequency\n4.Change contrast\n5.Change phase\n6.Chnage SOA frames\n7.Change prime type\n8.Change test type\n", 1)

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
    if prime_type ==1 :
        mask_inner = visual.Circle(win=win, radius=prime_size/2 , fillColor=bg_color, lineColor = bg_color)
    else:
        mask_inner = visual.Circle(win=win, radius=prime_size/2 , fillColor=bg_color, lineColor = 'black')
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
            if SOA_frame == 0:
                frames = [blank, mask_prime, mask]
                frameDurations = [fixation_frame, prime_frame, mask_frame-prime_frame] 
            elif SOA_frame == prime_frame: # prime_frame is set to 1
                frames = [blank, prime, mask]
                frameDurations = [fixation_frame, prime_frame, mask_frame] 
            elif SOA_frame > prime_frame:
                frames = [blank, prime, blank, mask]
                frameDurations = [fixation_frame, prime_frame, SOA_frame-prime_frame, mask_frame]

        stamps = exlib.runFrames(win, frames, frameDurations, trialClock)
        critTime = exlib.actualFrameDurations(frameDurations, stamps)[1]
        critPass = (np.absolute((prime_frame/refreshRate) - critTime) < .001)
        if not critPass:
            print('Critical pass fail, while critical time is ' + str(np.round(critTime, 4)) +
                  ', actual time is ' + str(np.round(prime_frame/refreshRate, 4)))
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
    again = input("Restart the experiment? (y/n): ").strip().lower()
    if again != "y":
        break

core.quit()
