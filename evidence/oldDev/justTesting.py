import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

# Function to define the transfer function
def transfer(m, crit, order=6):
    return 1 / (1 + (m / crit) ** order)

# Creating a blank image with specified dimensions
width, height = 256, 256
image = np.ones((height, width))  # Filling with white initially

# Adding text "A" at the center of the image
text = np.zeros_like(image)
plt.text(0.5*width, 0.5*height, "A", fontsize=60, ha='center', va='center', color='black')

# Inverting the text so it's white on black background
result = image - text

plt.imshow(result, cmap='gray', vmin=0, vmax=1)  # Ensure black and white display
plt.axis('off')  
plt.savefig('testA.png', bbox_inches='tight', pad_inches=0)
plt.show()

# Compute the FFT of the image
g = fft(result)
power = np.abs(g)
dim_g = g.shape

crit = 5
M = dim_g[0]
m = M // 4
coef = np.zeros(M)
coef[:m] = transfer(np.arange(1, m + 1), crit)
coef[M-m:] = transfer(np.arange(1, m + 1), crit)
filter_ = np.outer(coef, coef)
f = np.real(ifft(g * filter_, axis=0)) / np.prod(dim_g)

# Display the filtered image
plt.imshow(f, cmap='gray')
plt.axis('off')
plt.show()
