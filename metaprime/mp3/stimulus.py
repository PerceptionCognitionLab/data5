from psychopy import visual, core, monitors
import numpy as np
# Define your external monitor

monitor = monitors.Monitor("MyMonitor")
monitor.setSizePix((1920, 1080))
monitor.setWidth(60)
monitor.setDistance(60)
monitor.saveMon()


win = visual.Window(units="deg", monitor = monitor, size=(1920, 1080), color= (0, 0, 0), fullscr=True)

gabor = visual.GratingStim(
    win=win,
    tex = "sin",  # sinusoidal grating
    size = 5,  # diameter of 2 deg
    sf = 0.75,    # spatial frequency in cycles/deg 
    ori = -30,  # orientation in degrees
    pos = (-3.5, 0),  # position 3.5 deg left of fixation mark
    contrast = 1,
    mask = 'gauss'
)


mask = visual.GratingStim(
    win = win,
    tex = "sin",
    size = 7.5, 
    sf = 0.75, 
    ori = 30,  
    pos = (-3.5, 0),  
    contrast = 1,
    mask = 'circle',
)




blur_region = visual.GratingStim(
    win=win,
    tex=None,  # No texture, just a flat grey region
    size=12,  # Circle of radius 5
    sf=0,  # No spatial frequency
    pos=(-3.5, 0),  # Match position of the original grating
    mask="gauss",  # Uniform circular mask
    color=[0, 0, 0],  # Neutral grey
    contrast=0.2,  # Adjust to create the blur effect
)

    

# Composite the two masks using alpha blending

mask.draw()
blur_region.draw()  # Overlay the Gaussian envelope
gabor.draw()



# Display the stimuli
win.flip()

# Wait for a while to view the image
core.wait(5)

# Close the window
win.close()
