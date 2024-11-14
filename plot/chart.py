import config
import data
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button
import network.jsn_drop_service
import pandas as pd

jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)

def draw_figure(canvas, figure):
    """
    Draw a Matplotlib figure on a Tkinter Canvas.

    Args:
        canvas (Tk.Canvas): The Tkinter canvas to draw on.
        figure (FigureCanvasTkAgg): The Matplotlib figure object to be drawn.

    Returns:
        FigureCanvasTkAgg: The figure canvas object that allows further manipulation.
    """
    # Convert Matplotlib figure (i.e., a chart object) to FigureCanvasTkAgg object
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    # Drawing chart
    figure_canvas_agg.draw()
    # Place a Matplotlib chart in a Tkinter window and control how it is laid out.
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)  
    return figure_canvas_agg

# Need explanation
def delete_figure_agg(figure_agg):
    """
    Close and delete all Matplotlib figures.

    Args:
        figure_agg (FigureCanvasTkAgg): The figure canvas object to close and delete.

    Returns:
        None
    """
    figure_agg.get_tk_widget().pack_forget()
    plt.close('all')

# def print_placeholder():
#     """
#     Create a placeholder chart when there is no data to display.

#     Returns:
#         matplotlib.figure.Figure: A Matplotlib figure object with a placeholder chart.
#     """
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.text(0.5, 0.5, 'Chart Placeholder', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
#     # Hide the x and y axis ticks
#     ax.set_xticks([])
#     ax.set_yticks([]) 
#     return fig, ax

def draw_local_graph(file_path):
    """
    Draw bar plot according to local file
    Args:
        file_path (str): local file path
    """
    try:
        # Read data from file
        data = pd.read_csv(file_path)

        if 'City' in data.columns:
            fig, ax1 = plt.subplots(figsize=(10, 6))

            # Create first axis
            ax1.set_xlabel('Weather Parameters')
            ax1.set_ylabel('Temp & Humidity', color='blue')
            ax1.bar(['Temperature (°C)', 'Humidity (%)'], 
                    [data['Temperature (°C)'][0], data['Humidity (%)'][0]], 
                    color='blue', alpha=0.6, label='Temp & Humidity')
            ax1.tick_params(axis='y', labelcolor='blue')

            # Create second axis
            ax2 = ax1.twinx()
            ax2.set_ylabel('Wind Speed, Cloud Cover', color='red')
            ax2.bar(['Wind Speed (m/s)', 'Cloud info'], 
                    [data['Wind Speed (m/s)'][0], data['Cloud info'][0]], 
                    color='red', alpha=0.6, label='Wind, Cloud & Rain')
            ax2.tick_params(axis='y', labelcolor='red')

            # Add title and legend
            fig.suptitle('Current Weather with Dual Axes')
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')

            return fig, ax1
        elif 'Time' in data.columns:
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))

            data['Time'] = pd.to_datetime(data['Time'])
            # Draw line plot
            ax.plot(data['Time'], data['Temperature (°C)'], marker='o') # A function for drawing Line Chart

            # Set up title and label
            ax.set_title("Temperature forecast for the next 24 hours")
            ax.set_xlabel("Time") # A label of x-axiss
            ax.set_ylabel("Temp (°C)") # A label of y-axis
            
            # Make X axis tilt 45 degrees
            plt.xticks(rotation=45)
            
            # Add grid line
            plt.grid(True)
            return fig, ax
    except Exception as e:
        print("Oops! Something wrong: ", e)

def draw_remote_graph(file_path):

    pass

# I got idea from: https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
def draw_current_temperature(current_data):
    """
    Create a bar plot for current weather data.

    Args:
        current_data (dict): Current weather data got from the OpenWeather API.

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object with the current weather bar plot.
    """
    categories = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)', 'Cloud Cover (%)', 'Rain (mm)']

    current_temp_celsius = current_data["main"]["temp"] - 273.15
    current_humidity = current_data["main"]["humidity"]
    current_wind_speed = current_data["wind"]["speed"]
    current_cloud_cover = current_data["clouds"]["all"]
    # # Handle the case where rainfall may not exist
    current_rain = current_data.get("rain", {}).get("1h", 0)  
    
    values_1 = [current_temp_celsius, current_humidity]
    values_2 = [current_wind_speed, current_cloud_cover, current_rain]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.bar(categories[:2], values_1, color='blue', width=0.4, label="Temp & Humidity")
    ax1.legend()
    ax1.set_title("Current Weather with Dual Axes")
    ax1.set_xlabel('Weather Parameters')
    ax1.set_ylabel('Temp & Humidity', color='blue')

    # Draw another y axis of Bar Plot
    ax2 = ax1.twinx()
    ax2.bar(categories[2:], values_2, color='red', width=0.4, label="Wind, Cloud & Rain")
    ax2.legend()
    ax2.set_ylabel('Wind Speed, Cloud Cover & Rain', color='red')
    plt.tight_layout()
    # plt.show()
    return fig


def draw_forecast_temperature(forecast_data):
    """
    Create a line plot for the temperature forecast for next 24 hours.

    Args:
        forecast_data (dict): Forecast weather data got from the OpenWeather API.

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object with the temperature forecast line plot.
    """
    # Get time and temp data from API
    times = []
    temperatures = []
    
    # Weather data for the next 24 hours (one data point every 3 hours)
    for i in forecast_data["list"][:8]:  
        forecast_time = i["dt_txt"]
        forecast_temp = i["main"]["temp"] - 273.15 # Convert from Kelvin to Celsius
        times.append(forecast_time)
        temperatures.append(forecast_temp)

    # Passing data into line plot to draw chart
    fig = plt.figure(figsize=(10, 6)) # Create a new figure window and define size
    plt.plot(times, temperatures, marker='o') # A function for drawing Line Chart
    plt.xticks(rotation=45)
    plt.xlabel("Time") # A label of x-axis
    plt.ylabel("Temp (°C)") # A label of y-axis
    plt.title("Temperature forecast for the next 24 hours") # Title of Line Chart
    plt.grid(True) # Add grid line to help read
    plt.tight_layout() # Change the layout of chart automatically
    return fig


def zoom_in(ax1, ax2=None):
    try:
        xlim = ax1.get_xlim()
        ylim = ax1.get_ylim()
        
        # Zoom in the graph
        # The range of display is reduced
        # xlim = [0, 10] -> [2, 8] 
        new_xlim = [xlim[0] + (xlim[1] - xlim[0]) * (1 - 1/config.scale_factor) / 2,
                    xlim[1] - (xlim[1] - xlim[0]) * (1 - 1/config.scale_factor) / 2]
        # ylim = [0, 10] -> [2, 8]
        new_ylim = [ylim[0] + (ylim[1] - ylim[0]) * (1 - 1/config.scale_factor) / 2,
                    ylim[1] - (ylim[1] - ylim[0]) * (1 - 1/config.scale_factor) / 2]
        
        ax1.set_xlim(new_xlim)
        ax1.set_ylim(new_ylim)

        if ax2:
            ylim2 = ax2.get_ylim()
            new_ylim2 = [ylim2[0] + (ylim2[1] - ylim2[0]) * (1 - 1/config.scale_factor) / 2,
                        ylim2[1] - (ylim2[1] - ylim2[0]) * (1 - 1/config.scale_factor) / 2]
            ax2.set_ylim(new_ylim2)

        # I got this code from: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.draw.html
        ax1.figure.canvas.draw_idle()
    except Exception as e:
        print("Oops! Something wrong: ", e)

def zoom_out(ax1, ax2=None):
    try:
        xlim = ax1.get_xlim()
        ylim = ax1.get_ylim()
        
        # Zoom out the graph
        # The range of display is increased
        # xlim = [0, 10] -> [-2, 12]
        new_xlim = [xlim[0] - (xlim[1] - xlim[0]) * (config.scale_factor - 1) / 2,
                    xlim[1] + (xlim[1] - xlim[0]) * (config.scale_factor - 1) / 2]
        # ylim = [0, 10] -> [-2, 12]
        new_ylim = [ylim[0] - (ylim[1] - ylim[0]) * (config.scale_factor - 1) / 2,
                    ylim[1] + (ylim[1] - ylim[0]) * (config.scale_factor - 1) / 2]
        
        ax1.set_xlim(new_xlim)
        ax1.set_ylim(new_ylim)

        if ax2:
            ylim2 = ax2.get_ylim()
            new_ylim2 = [ylim2[0] - (ylim2[1] - ylim2[0]) * (config.scale_factor - 1) / 2,
                        ylim2[1] + (ylim2[1] - ylim2[0]) * (config.scale_factor - 1) / 2]
            ax2.set_ylim(new_ylim2)

        ax1.figure.canvas.draw_idle()
    except Exception as e:
        print("Oops! Something wrong: ", e)

# def main():
#     current_data, forecast_data = data.get_weather_data()
#     if current_data:
#         draw_current_temperature(current_data)
#     else:
#         print("Getting current weather data fail!")

#     if forecast_data:
#         draw_forecast_temperature(forecast_data)
#     else:
#         print("Getting weather forecast data fail!")