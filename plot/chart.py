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
    try:
        # Convert Matplotlib figure (i.e., a chart object) to FigureCanvasTkAgg object
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        # Drawing chart on Canvas control
        figure_canvas_agg.draw()
        # Place a Matplotlib chart in a Tkinter window and control how it is laid out.
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)  
        return figure_canvas_agg
    except Exception as e:
        print("This is error message: ", e)    
    

# Need explanation
def delete_figure_agg(figure_agg):
    """
    Close and delete all Matplotlib figures.

    Args:
        figure_agg (FigureCanvasTkAgg): The figure canvas object to close and delete.

    Returns:
        None
    """
    try:
        figure_agg.get_tk_widget().pack_forget()
        plt.close('all')
    except Exception as e:
        print("This is error message: ", e)

def print_placeholder():
    """
    Create a placeholder chart when there is no data to display.

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object with a placeholder chart.
    """
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.text(0.5, 0.5, 'Chart will display here, you should load/upload data first and click "DRAW" button to display plot.', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        # Hide the x and y axis ticks
        ax.set_xticks([])
        ax.set_yticks([]) 
        return fig, ax
    except Exception as e:
        print("This is error message: ", e)

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
        elif 'Date' in data.columns:
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))

            data['Date'] = pd.to_datetime(data['Date'])
            # Draw line plot
            ax.plot(data['Date'], data['Temperature (°C)'], marker='o', label='Original Data')

            # Set up title and label
            ax.set_title("Temperature forecast for the next 24 hours")
            ax.set_xlabel("Date") # A label of x-axiss
            ax.set_ylabel("Temp (°C)") # A label of y-axis
            
            # Make X axis tilt 45 degrees
            plt.xticks(rotation=45)
            # Add grid line
            plt.grid(True)

            return fig, ax
    except Exception as e:
        print("Oops! Something wrong: ", e)

def draw_merge_graph(file_path, merge_file_path):
    try:
        original_data = pd.read_csv(file_path)
        merged_data = pd.read_csv(merge_file_path)
        
        fig, ax = plt.subplots(figsize=(10, 6))

        original_data['Date'] = pd.to_datetime(original_data['Date'])
        merged_data['Date'] = pd.to_datetime(merged_data['Date'])

        # Convert date format
        ax.plot(original_data['Date'], original_data['Temperature (°C)'], color = 'blue', label="Original Data")
        ax.plot(merged_data['Date'], merged_data['Temperature (°C)'], color = 'red', label="Merged Data", linestyle="--")

        ax.legend()
        ax.grid()
        ax.set_title("Original and Merged Data Comparison")
        
        return fig, ax
    except Exception as e:
        print(f"Error in draw_merge_graph: {e}")
        return None


# I got idea from: https://www.geeksforgeeks.org/bar-plot-in-matplotlib/
def draw_current_data_from_remote(result):
    """
    Create current weather data plot based on data from JsnDrop

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object with the current weather bar plot.
    """
    try:
        if result:
            temperature = result["temperature"]
            humidity = result["humidity"]
            wind = result["wind"]
            cloud = result["cloud"]

            fig, ax1 = plt.subplots(figsize=(10, 6))

            # Create first axis
            ax1.set_xlabel('Weather Parameters')
            ax1.set_ylabel('Temp & Humidity', color='blue')
            ax1.bar(['Temperature (°C)', 'Humidity (%)'], 
                    [temperature, humidity], 
                    color='blue', alpha=0.6, label='Temp & Humidity')
            ax1.tick_params(axis='y', labelcolor='blue')

            # Create second axis
            ax2 = ax1.twinx()
            ax2.set_ylabel('Wind Speed, Cloud Cover', color='red')
            ax2.bar(['Wind Speed (m/s)', 'Cloud info'], 
                    [wind, cloud], 
                    color='red', alpha=0.6, label='Wind, Cloud & Rain')
            ax2.tick_params(axis='y', labelcolor='red')

            # Add title and legend
            fig.suptitle('Current Weather with Dual Axes')
            ax1.legend(loc='upper left')
            ax2.legend(loc='upper right')

            return fig, ax1
        else:
            return None
    except Exception as e:
        print("Error message:", e)
        return None


def draw_forecast_data_from_remote(result):
    """
    Create forecast weather data plot based on data from JsnDrop

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object with the temperature forecast line plot.
    """
    try:
        if result:
            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Extract all date and temperature from result, is a list comprehension
            dates = [entry["Date"] for entry in result]
            formatted_date = pd.to_datetime(dates)

            # Convert temperature to float
            temperatures = [float(entry["Temperature"]) for entry in result]

            # Create chart
            fig, ax = plt.subplots(figsize=(10, 6))

            # Draw line plot
            ax.plot(formatted_date, temperatures, marker='o')

            # Set up title and label
            ax.set_title("Temperature forecast for the next 24 hours")
            ax.set_xlabel("Date")
            ax.set_ylabel("Temp (°C)")
            
            # Make X axis tilt 45 degrees
            plt.xticks(rotation=45)
            
            # Add grid line
            plt.grid(True)
            return fig, ax
        else:
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None


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