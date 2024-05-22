import numpy as np
from numpy import random
from psychopy import core, visual, event
from PIL import Image

# Initialize random number generator
rng = random.default_rng(seed=np.random.randint(1, 1000, 1))

# Create a window
win = visual.Window(units="pix", size=(750, 750), color=[1, 1, 1], fullscr=True)

# Function to draw a random monochrome letter
def rand_ltr():
    mono_W = np.flip(np.array(Image.open('testW.png').convert("L"))) / 255.0
    mono_A = np.flip(np.array(Image.open('testA.png').convert("L"))) / 255.0
    mono_M = np.flip(np.array(Image.open('testM.png').convert("L"))) / 255.0
    mono_O = np.flip(np.array(Image.open('testO.png').convert("L"))) / 255.0
    letters = [("A", mono_A), ("W", mono_W), ("M", mono_M), ("O", mono_O)]
    select = rng.integers(0, 4)
    chosen_letter, chosen_ltr_image = letters[select]
    stim = visual.ImageStim(win, image=chosen_ltr_image)
    stim.draw()
    return stim, chosen_letter

# # Function to get the response
# def get_response(chosen_letter):
#     continueRoutine = True
#     response_list = []
#     response = 0
#     while continueRoutine:
#         keys = event.waitKeys()
#         response_list.extend(keys)
#         if chosen_letter in response_list:
#             response = 1  # True
#             continueRoutine = False
#         elif any(key in ['escape', 'q'] for key in response_list):
#             response = 0  # False
#             continueRoutine = False
#     return response

# Main test function
def test_image(duration=3):
    stim, chosen_letter = rand_ltr()
    win.flip()
    # response_accuracy = get_response(chosen_letter)
    core.wait(duration)
    win.close()
    # print(f"Chosen letter: {chosen_letter}, Response accuracy: {response_accuracy}")

# Run the test
test_image()
core.quit()

