import sys
sys.path.insert(0, '/home/exp/specl-exp/lib/data5/')
import expLib51 as exlib
from psychopy import visual, core, event
import pandas as pd

# === Setup ===
win = visual.Window(size=(1920, 1080), color=(0, 0, 0), units='norm', fullscr=True)
stim = visual.Rect(win, width=2, height=2)

# Data storage
data = []

# Define color channels
colors = ['red', 'green', 'blue']

# Loop through each color channel
for color in colors:
    for value in range(0, 256, 16):
        rgb = [0, 0, 0]
        if color == 'red':
            rgb[0] = value / 255
        elif color == 'green':
            rgb[1] = value / 255
        elif color == 'blue':
            rgb[2] = value / 255
        
        stim.fillColor = rgb
        stim.draw()
        win.flip()
        
        # Input prompt
        typed_text = ''
        input_complete = False
        text_stim = visual.TextStim(win, text='', pos=(0, -0.8), color=(1, 1, 1), height=0.07)
        
        while not input_complete:
            stim.draw()
            text_stim.text = f"Enter illuminance for {color} {value}: {typed_text}"
            text_stim.draw()
            win.flip()
            
            keys = event.waitKeys()
            for key in keys:
                if key == 'escape':
                    win.close()
                    core.quit()
                elif key == 'return':
                    input_complete = True
                elif key == 'backspace':
                    typed_text = typed_text[:-1]
                elif key in ['0','1','2','3','4','5','6','7','8','9']:
                    typed_text += key
                elif key == 'minus' and len(typed_text) == 0:
                    typed_text += '-'
                elif key == 'period' and '.' not in typed_text:
                    typed_text += '.'
        
        # Store result
        try:
            illuminance = float(typed_text)
        except ValueError:
            illuminance = None  # handle if input is invalid
        
        data.append({
            'color': color,
            'intensity': value,
            'illuminance': illuminance
        })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv('stimulus_illuminance_all_colors.csv', index=False)

win.close()
core.quit()



import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv('stimulus_illuminance_all_colors.csv')

# Normalize intensity (0 to 1)
df['intensity_norm'] = df['intensity'] / 255.0

# Define the gamma function
def gamma_func(I, a, gamma):
    return a * (I ** gamma)

# Store results
results = {}

# Fit for each color channel
for color in ['red', 'green', 'blue']:
    color_data = df[df['color'] == color]
    I = color_data['intensity_norm'].values
    L = color_data['illuminance'].values

    # Remove any NaNs
    valid = ~np.isnan(I) & ~np.isnan(L)
    I = I[valid]
    L = L[valid]

    # Fit curve
    popt, pcov = curve_fit(gamma_func, I, L, bounds=(0, [np.inf, 5]))
    a_fit, gamma_fit = popt
    results[color] = {'a': a_fit, 'gamma': gamma_fit}

    # Plot
    plt.figure()
    plt.scatter(I, L, label='Measured')
    I_fit = np.linspace(0, 1, 100)
    L_fit = gamma_func(I_fit, *popt)
    plt.plot(I_fit, L_fit, color='red', label=f'Fit γ={gamma_fit:.2f}')
    plt.title(f'{color.capitalize()} Channel Gamma Fit')
    plt.xlabel('Normalized Intensity')
    plt.ylabel('Illuminance')
    plt.legend()
    plt.grid(True)
    plt.show()

# Print gamma values
for color, params in results.items():
    print(f"{color.capitalize()} - Gamma: {params['gamma']:.3f}, a: {params['a']:.3f}")



import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('stimulus_illuminance_all_colors.csv')

# Plot settings
channels = ['red', 'green', 'blue']
colors = {'red': 'red', 'green': 'green', 'blue': 'blue'}

# Create one plot per channel
for channel in channels:
    channel_data = df[df['color'] == channel]
    plt.figure()
    plt.scatter(channel_data['intensity'], channel_data['illuminance'], color=colors[channel])
    plt.title(f'{channel.capitalize()} Channel: Intensity vs Illuminance')
    plt.xlabel('Intensity (0–255)')
    plt.ylabel('Illuminance (lux)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
