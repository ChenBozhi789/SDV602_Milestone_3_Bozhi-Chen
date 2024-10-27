import requests
import matplotlib.pyplot as plt
from datetime import datetime

def get_weather_data():
    """
    Get current weather data and forecast weather data for next 5 days from OpenWeather API.

    Returns:
        tuple: A tuple containing:
            - current_data (dict or None): Current weather data if the request is successful, otherwise None.
            - forecast_data (dict or None): Forecast weather data if the request is successful, otherwise None.
    """
    # Define the API key and endpoint
    API_KEY = '2a86ef82b86f547e5b33df59dea5b840'  # Replace with your OpenWeather API key
    lat = '-41.270634'  # Latitude for the location
    lon = '173.283966'  # Longitude for the location

    # Call current weather data
    url_current = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
    # Call 5 day / 3 hour forecast data
    url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}'


    # Send the GET request to the API
    current_response = requests.get(url_current)
    current_data = current_response.json() if current_response.status_code == 200 else None

    forecast_response = requests.get(url_forecast)
    forecast_data = forecast_response.json() if forecast_response.status_code == 200 else None

    return current_data, forecast_data

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

def print_placeholder():
    """
    Create a placeholder chart when there is no data to display.

    Returns:
        matplotlib.figure.Figure: A Matplotlib figure object with a placeholder chart.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.5, 0.5, 'Chart Placeholder', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    # Hide the x and y axis ticks
    ax.set_xticks([])
    ax.set_yticks([]) 
    return fig

def main():
    current_data, forecast_data = get_weather_data()
    if current_data:
        draw_current_temperature(current_data)
    else:
        print("Getting current weather data fail!")

    if forecast_data:
        draw_forecast_temperature(forecast_data)
    else:
        print("Getting weather forecast data fail!")
    

if __name__ == "__main__":
    main()