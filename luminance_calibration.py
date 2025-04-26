import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as exlib
from psychopy import visual, core, event
import pandas as pd

# === Setup ===
win = visual.Window(size=(500,500), color=(0, 0, 0), units='pix', fullscr=False, monitor='MyMonitor')

# Define the flicker gray pairs (low_gray, high_gray)
flash_pairs = [
    (0, 255),
    (32, 255),
    (64, 255),
    (96, 255),
    (128, 255),
    (0, 128),
    (32, 128),
    (64, 128),
    (96, 128)
]

matched_results = []

# === Main loop ===
for low_gray, high_gray in flash_pairs:
    bg_gray = 128  # Initial inner background gray
    expected_gray = (low_gray + high_gray) / 2  # Theoretical mean
    adjusting = True

    while adjusting:
        # Fill the outer background as black
        win.color = [0, 0, 0]

        # Define the grid area
        grid_width = 500   # grid size
        grid_height = 500
        n_lines_x = 500     # number of vertical lines

        line_width = grid_width / n_lines_x
        line_height = grid_height

        start_x = -grid_width / 2 + line_width / 2  # center the grid

        # Draw vertical lines
        for i in range(n_lines_x):
            x_pos = start_x + i * line_width
            this_line_gray = low_gray if i % 2 == 0 else high_gray
            this_line_color = (this_line_gray / 255) * 2 - 1

            line = visual.Rect(
                win,
                width=line_width * 0.8,
                height=line_height,
                pos=(x_pos, 0),
                fillColor=[this_line_color]*3,
                lineColor=[this_line_color]*3
            )
            line.draw()

        # Draw the adjustable center patch
        inner_color = (bg_gray / 255) * 2 - 1
        center_patch = visual.Rect(
            win,
            width=grid_width * 0.5,
            height=grid_height * 0.5,
            pos=(0, 0),
            fillColor=[inner_color]*3,
            lineColor=[inner_color]*3
        )
        center_patch.draw()

        # Show current info: expected and current
        info_text = visual.TextStim(
            win,
            text=f"Expected luminance: {expected_gray:.1f}\nCurrent luminance: {bg_gray}",
            pos=(0, -200),
            color='black',
            height=30,
            alignText='center'
        )
        info_text.draw()

        # Flip window
        win.flip()

        # Check for keypress
        keys = event.getKeys(keyList=['left', 'right', 'space', 'escape'])

        for key in keys:
            if key == 'left':
                bg_gray = max(0, bg_gray - 2)  # Decrease brightness
            elif key == 'right':
                bg_gray = min(255, bg_gray + 2)  # Increase brightness
            elif key == 'space':
                matched_results.append((low_gray, high_gray, bg_gray))
                adjusting = False
            elif key == 'escape':
                win.close()
                core.quit()

# Close window
win.close()

# === Save results to CSV ===
df = pd.DataFrame(matched_results, columns=['low_gray', 'high_gray', 'matched_inner_gray'])
df['expected_gray'] = (df['low_gray'] + df['high_gray']) / 2
df.to_csv('gamma_subjective_inner_patch1.csv', index=False)

print("Measurement complete! Results saved to 'gamma_subjective_inner_patch.csv'.")
print(df)
