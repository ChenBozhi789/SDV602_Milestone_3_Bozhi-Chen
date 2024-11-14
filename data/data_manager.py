import config
from datetime import datetime
import network.jsn_drop_service
import requests
import pandas as pd
import PySimpleGUI as sg

jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)

def initialize_database():
    print("Start initializing remote database...")
    print("-" * 50)

    # Create tbUser table in JsnDrop database when first open
    check_tbUser = jsn.all(config.user_table)
    if check_tbUser == "Data error. JsnTable 'tbUser' does not exist":
        create_result = jsn.create(config.user_table, config.tbUser_example)
        if create_result == 'create tbUser executed':
            print("Create tbUser successfully!")
            print("-" * 50)
    else:
        print("tbUser already exists!")
        print("-" * 50)

    # Create tbCurrentData table in JsnDrop database when first open
    check_tbCurrentData = jsn.all(config.current_data_table)
    if check_tbCurrentData == "Data error. JsnTable 'tbCurrentData' does not exist":
        create_result = jsn.create(config.current_data_table, config.tbCurrentData_example)
        if create_result == 'create tbCurrentData executed':
            print("Create tbCurrentData successfully!")
            print("-" * 50)
    else:
        print("tbCurrentData already exists!")
        print("-" * 50)

    # Create tbForecastData table in JsnDrop database when first open
    check_tbForecastData = jsn.all(config.forecast_data_table)
    if check_tbForecastData == "Data error. JsnTable 'tbForecastData' does not exist":
        create_result = jsn.create(config.forecast_data_table, config.tbForecastData_example)
        if create_result == 'create tbForecastData executed':
            print("Create tbForecastData successfully!")
            print("-" * 50)
    else:
        print("tbForecastData already exists!")
        print("-" * 50)



def get_weather_data():
    """
    Get current weather data and forecast weather data for next 5 days from OpenWeather API.

    Returns:
        tuple: A tuple containing:
            - current_data (dict or None): Current weather data if the request is successful, otherwise None.
            - forecast_data (dict or None): Forecast weather data if the request is successful, otherwise None.
    """
    # Define the API key and endpoint
    API_KEY = '2a86ef82b86f547e5b33df59dea5b840'
    lat = '-41.270634'
    lon = '173.283966'

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

def load_local_data():
    file_path = sg.popup_get_file('Select file as file path')
    if file_path:
        print("File selected successfully:", file_path)
        return file_path
    else:
        print("Upload file fail")
        return None

def read_local_data(file_path):
    """
    Read weather data from local csv file
    Arg:
        The file path

    Returns:
        The data from the local csv file

    """
    try:
        reading_data = pd.read_csv(file_path)
        print("Data loaded successfully")
        return reading_data
    except Exception as e:
        print("Something wrong during reading data", e)
        return None
    
# This method is for current data
def store_current_to_remote():
    try:
        current_data, forecast_data = get_weather_data()
        weather_data = {
            # Serialize datetime object to string
            "Date": datetime.fromtimestamp(current_data["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
            "temperature": round(current_data["main"]["temp"] - 273.15, 2),
            "humidity": current_data["main"]["humidity"],
            "description": current_data["weather"][0]["description"]
        }

        jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)
        store_result = jsn.store(config.current_data_table, [weather_data])

        if store_result == "STORE tbCurrentData executed":
            print("Current weather data stored successfully!")
            print("-" * 50)
            return True
        else:
            print("Failed to store current weather data!")
            print("-" * 50)
            return False
    except Exception as e:
        print("Error: ", e)

def store_forecast_to_remote():
    try:
        current_data, forecast_data = get_weather_data()
        forecast_weather_list = []

        for i in forecast_data['list'][:8]:
            weather_data = {
                # Serialize datetime object to string
                "Date": datetime.fromtimestamp(i["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
                "temperature": round(i["main"]["temp"] - 273.15, 2),
            }
            forecast_weather_list.append(weather_data)
        
        jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)
        store_result = jsn.store(config.forecast_data_table, forecast_weather_list)

        if store_result == "STORE tbForecastData executed":
            print("Forecast weather data stored successfully!")
            print("-" * 50)
            return True
        else:
            print("Failed to store forecast weather data!")
            print("-" * 50)
            return False
    except Exception as e:
        print("Error: ", e)