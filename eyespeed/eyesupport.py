import matplotlib.pyplot as plt

def save_letter_image(letter, filename):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(3, 3), dpi=256/3)

    # Set margins to zero
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Remove the axes
    ax.axis('off')

    # Add the letter text
    ax.text(0.5, 0.5, letter, fontsize=100, ha='center', va='center')

    # Save the figure
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close()

# Save the letter 'M'
save_letter_image('M', 'testM.png')

# Save the letter 'W'
save_letter_image('W', 'testW.png')
save_letter_image('A', 'testA.png')
save_letter_image('O', 'testO.png')