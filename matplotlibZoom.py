import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np

# Function to draw the Matplotlib figure on a PySimpleGUI canvas


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Function to add the Matplotlib toolbar with zoom and pan to PySimpleGUI canvas


def add_toolbar(canvas, figure_canvas_agg):
    toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas)
    toolbar.update()
    toolbar.pack(side='top', fill='both', expand=1)


# Set up PySimpleGUI layout with a Canvas element
layout = [
    [sg.Text("Matplotlib Plot with Zoom and Pan")],
    [sg.Canvas(key='-CANVAS-')],
    [sg.Button("Exit")]
]

# Create the PySimpleGUI window
window = sg.Window("Zoom and Pan with Matplotlib", layout, finalize=True)

# Generate a sample Matplotlib plot
fig, ax = plt.subplots()
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.plot(x, y)
ax.set_title("Sine Wave")

# Draw the figure and add the toolbar
canvas_elem = window['-CANVAS-']
canvas = canvas_elem.TKCanvas
fig_canvas_agg = draw_figure(canvas, fig)
add_toolbar(canvas, fig_canvas_agg)

# Event loop for PySimpleGUI window
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

# Close the GUI
window.close()
