import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import random
from psychopy import core, visual, sound, event, clock
import eyesupport
from PIL import Image

rng = random.default_rng(seed = np.random.randint(1,1000,1))
mono_W = np.flip(np.array(Image.open('testW.png').convert("L"))) / 255.0
mono_A = np.flip(np.array(Image.open('testA.png').convert("L"))) / 255.0
win = visual.Window(units="pix", size=(750, 750), color=[1,1,1], fullscr=True)


def rand_ltr():
    select = rng.integers(0, 2)
    print('if "0" then "a" if "1" then "w":',select)
    if select == 0:
        stim = visual.ImageStim(win, image = mono_A)
    if select == 1:
        stim = visual.ImageStim(win, image = mono_W)
    stim.draw()
    return stim


def test_image(duration=3):
    rand_ltr()
    win.flip()
    core.wait(duration)
    win.close()


test_image()

