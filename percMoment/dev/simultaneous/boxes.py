from psychopy import core, visual

win = visual.Window(size=(800, 600), color=[1, 1, 1], units='norm')

abortKey=['9']

# A Textbox stim that will look similar to a TextStim component

textstimlike=visual.TextBox(
    window=win,
    text="This textbox looks most like a textstim.",
    font_size=18,
    font_color=[-1,-1,1],
    color_space='rgb',
    size=(1.8,.1),
    pos=(0.0,.5),
    units='norm')

textboxloaded=visual.TextBox(
    window=win,
    text="TextBox showing all supported graphical elements",
    font_size=32,
    font_color=[1,1,1],
    border_color=[-1,-1,1], # draw a blue border around stim
    border_stroke_width=4, # border width of 4 pix.
    background_color=[-1,-1,-1], # fill the stim background
    grid_stroke_width=1,  # with a width of 1 pix
    textgrid_shape=[20,2],  # specify area of text box
                            # by the number of cols x
                            # number of rows of text to support
                            # instead of by a screen
                            # units width x height.
    pos=(0.0,-.5),
    # If the text string length < num rows * num cols in
    # textgrid_shape, how should text be justified?
    #
    grid_horz_justification='center',
    grid_vert_justification='center')

textstimlike.draw()
textboxloaded.draw()
win.flip()
core.wait(5)

# Close the window and quit
win.close()
core.quit()

