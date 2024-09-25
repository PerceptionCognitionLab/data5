from psychopy import core, visual, event
import csv
import random

# Setup window
win = visual.Window(size=(1200, 800), color=[-1, -1, -1], fullscr=False, units="pix")
mouse = event.Mouse(visible=True, win=win)

# Setup video stimulus (from the hitter's view)
video_paths = ['hitter_pitch_1.mp4', 'hitter_pitch_2.mp4', 'hitter_pitch_3.mp4']  # Replace with actual hitter view video paths
videos = [visual.MovieStim3(win, video) for video in video_paths]

# Setup zones in the strike area
zones = {
    'HighInside': [-300, 0, 0, 300],  
    'HighMiddle': [0, 0, 300, 300],
    'HighOutside': [300, 0, 600, 300],
    'LowInside': [-300, -300, 0, 0],
    'LowMiddle': [0, -300, 300, 0],
    'LowOutside': [300, -300, 600, 0]
}

# Function to check which zone was clicked
def get_clicked_zone(mouse_pos):
    for label, coords in zones.items():
        if coords[0] <= mouse_pos[0] <= coords[2] and coords[1] <= mouse_pos[1] <= coords[3]:
            return label
    return None

# Function to draw zones
def draw_zones():
    for label, coords in zones.items():
        zone_rect = visual.Rect(win, width=coords[2] - coords[0], height=coords[3] - coords[1],
                                lineColor='white', pos=((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2))
        zone_rect.draw()

# Data storage
sid = 1  # Subject ID
data_filename = f'subject_{sid}_mlb_hitter_view.csv'
data_file = open(data_filename, 'w', newline='')
csv_writer = csv.writer(data_file)
csv_writer.writerow(['Trial', 'Video', 'PredictedZone', 'ReactionTime', 'Result'])

# Run trials
for trial, video in enumerate(videos):
    # Play video
    video.play()
    while video.status != visual.FINISHED:
        video.draw()
        win.flip()

    # Show the zones and wait for a click
    draw_zones()
    win.flip()

    # Collect response
    trial_clock = core.Clock()
    response = None
    while response is None:
        if mouse.getPressed()[0]:  # Left mouse click
            response_pos = mouse.getPos()
            guessed_zone = get_clicked_zone(response_pos)
            reaction_time = trial_clock.getTime()
            if guessed_zone is not None:
                response = True

    # Determine result (for demonstration, randomly assign correct zone)
    actual_zone = random.choice(list(zones.keys()))
    result = 'Correct' if guessed_zone == actual_zone else 'Incorrect'

    # Save data
    csv_writer.writerow([trial, video.filename, guessed_zone, reaction_time, result])

    # Feedback
    feedback_text = f"Actual Zone: {actual_zone}\nReaction Time: {reaction_time:.3f} sec\nResult: {result}"
    feedback = visual.TextStim(win, text=feedback_text, color='white', pos=(0, 0))
    feedback.draw()
    win.flip()
    core.wait(1)

# Close data file
data_file.close()

# End of experiment
thanks = visual.TextStim(win, text="Thank you for participating!\nPress any key to exit.", color='white')
thanks.draw()
win.flip()
event.waitKeys()
win.close()
core.quit()