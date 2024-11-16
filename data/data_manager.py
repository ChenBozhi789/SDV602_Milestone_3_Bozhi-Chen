import config
from datetime import datetime
import network.jsn_drop_service
import requests
import pandas as pd
import PySimpleGUI as sg

jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)

def initialize_database():
    try:
        print("Start initializing remote database...")

        # Create tbUser table in JsnDrop database when first open
        check_tbUser = jsn.all(config.user_table)
        if check_tbUser == "Data error. JsnTable 'tbUser' does not exist":
            create_result = jsn.create(config.user_table, config.tbUser_example)
            if create_result == 'create tbUser executed':
                print("Create tbUser successfully!")
        else:
            print("tbUser already exists!")

        # Create tbCurrentData table in JsnDrop database when first open
        check_tbCurrentData = jsn.all(config.current_data_table)
        if check_tbCurrentData == "Data error. JsnTable 'tbCurrentData' does not exist":
            create_result = jsn.create(config.current_data_table, config.tbCurrentData_example)
            if create_result == 'create tbCurrentData executed':
                print("Create tbCurrentData successfully!")
        else:
            print("tbCurrentData already exists!")

        # Create tbForecastData table in JsnDrop database when first open
        check_tbForecastData = jsn.all(config.forecast_data_table)
        if check_tbForecastData == "Data error. JsnTable 'tbForecastData' does not exist":
            create_result = jsn.create(config.forecast_data_table, config.tbForecastData_example)
            if create_result == 'create tbForecastData executed':
                print("Create tbForecastData successfully!")
        else:
            print("tbForecastData already exists!")

        # Create tbChat table in JsnDrop database when first open
        check_tbChat = jsn.all(config.chat_table)
        if check_tbChat == "Data error. JsnTable 'tbChat' does not exist":
            create_result = jsn.create(config.chat_table, config.tbChat_example)
            if create_result == 'create tbChat executed':
                print("Create tbChat successfully!")
        else:
            print("tbChat already exists!")
    except Exception as e:
        print("This is error message: ", e)        


def get_weather_data():
    """
    Get current weather data and forecast weather data for next 5 days from OpenWeather API.

    Returns:
        tuple: A tuple containing:
            - current_data (dict or None): Current weather data if the request is successful, otherwise None.
            - forecast_data (dict or None): Forecast weather data if the request is successful, otherwise None.
    """
    try: 
        # Send the GET request to the API
        current_response = requests.get(config.url_current)
        current_data = current_response.json() if current_response.status_code == 200 else None

        forecast_response = requests.get(config.url_forecast)
        forecast_data = forecast_response.json() if forecast_response.status_code == 200 else None

        return current_data, forecast_data
    except Exception as e:
        print("This is error message: ", e)    

def load_local_data():
    try:
        file_path = sg.popup_get_file('Select file as file path')
        if file_path:
            print("File selected successfully:", file_path)
            return file_path
        else:
            print("Upload file fail")
            return None
    except Exception as e:
        print("This is error message: ", e)

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
    
def get_user_data():
    try:
        check_user_result = jsn.select(config.user_table, f"UserID = '{config.register_id}'")
        return check_user_result
    except Exception as e:
        print("This is error message: ", e)
    

def get_current_weather_data():
    try:
        result = jsn.all(config.current_data_table)
        if result:
            return {
                "temperature": float(result[0]['Temperature']),
                "humidity": float(result[0]['Humidity']),
                "wind": float(result[0]['Wind']),
                "cloud": float(result[0]['Cloud'])
            }
        else:
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None

def get_forecast_weather_data():
    try:
        result = jsn.all(config.forecast_data_table)
        if result:
            forecast_list = []
            for i in result:
                formatted_data = {
                    "Date": i["Date"],
                    "Temperature": i['Temperature']
                }
                forecast_list.append(formatted_data)
            return forecast_list
        else:
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None

def upload_data_to_remote():
    try:
        # Get data from API
        current_data, forecast_data = get_weather_data()

        weather_data = {
            # Serialize datetime object to string
            "City": current_data["name"],
            "Temperature (°C)": round(current_data["main"]["temp"] - 273.15, 2),
            "Humidity (%)": current_data["main"]["humidity"],
            'Wind Speed (m/s)': current_data['wind']['speed'],
            'Cloud info': current_data["clouds"]["all"]
        }

        store_result = jsn.store(config.current_data_table, [weather_data])

        if store_result == "STORE tbCurrentData executed":
            print("Current weather data stored successfully!")
        else:
            print("Failed to store current weather data!")

        # Get forecast data
        forecast_weather_list = []

        for i in forecast_data['list'][:8]:
            weather_data = {
                # Serialize datetime object to string
                "Date": datetime.fromtimestamp(i["dt"]).strftime('%Y-%m-%d %H:%M:%S'),
                "Temperature (°C)": round(i["main"]["temp"] - 273.15, 2),
            }
            forecast_weather_list.append(weather_data)
        
        store_result = jsn.store(config.forecast_data_table, forecast_weather_list)

        if store_result == "STORE tbForecastData executed":
            print("Forecast weather data stored successfully!")
            return True
        else:
            print("Failed to store forecast weather data!")
            return False
    except Exception as e:
        print("Error: ", e)

def upload_current_data_to_remote(data):
    try:
        # iterrows() provided by Pandas
        for iedex, row in data.iterrows():
            formatted_data = {
            "City": row["City"],
            "Temperature (°C)": row["Temperature (°C)"],
            "Humidity (%)": row["Humidity (%)"],
            'Wind Speed (m/s)': row["Wind Speed (m/s)"],
            'Cloud info': row["Cloud info"]
            }                        

        store_result = jsn.store(config.current_data_table, [formatted_data])

        if store_result == "STORE tbCurrentData executed":
            print("Current weather data stored successfully!")
            return True
        else:
            print("Failed to store current weather data!")
            return False
    except Exception as e:
        print("Error: ", e)

def upload_forecast_data_to_remote(data):
    try:
        forecast_weather_list = []

        # iterrows() provided by Pandas
        for iedex, row in data.iterrows():
            formatted_data = {
                "Date": row["Date"],
                "Temperature (°C)": row["Temperature (°C)"]
            }                        
            forecast_weather_list.append(formatted_data)
        
        store_result = jsn.store(config.forecast_data_table, forecast_weather_list)

        if store_result == "STORE tbForecastData executed":
            print("Forecast weather data stored successfully!")
            return True
        else:
            print("Failed to store forecast weather data!")
            return False
    except Exception as e:
        print("Error message: ", e)

def download_data_as_csv():
    try:
        # Get current weather data and save as csv file
        current_response = requests.get(config.url_current)

        if current_response.status_code == 200:
            # Parse data to json file
            current_data = current_response.json()
            weather_data = {
                'City': current_data['name'],
                'Temperature (°C)': round(current_data['main']['temp'] - 273.15, 2),
                'Humidity (%)': current_data['main']['humidity'],
                'Wind Speed (m/s)': current_data['wind']['speed'],
                'Cloud info': current_data["clouds"]["all"]
            }

            df = pd.DataFrame([weather_data])
            df.to_csv('nelson_weather.csv', index=False)
            print('Weather current data has been saved as nelson_weather.csv')
        else:
            print(f'Request fail, states code: {current_response.status_code}')

        # # Get forecast weather data and save as csv file
        forecast_response = requests.get(config.url_forecast)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            forecast_weather_list = []

            for i in forecast_data['list'][:8]:
                # Parse data to json file
                weather_data = {    
                    'Date': i['dt_txt'],
                    'Temperature (°C)': round(i["main"]["temp"] - 273.15, 2)
                }
                forecast_weather_list.append(weather_data)

            df = pd.DataFrame(forecast_weather_list)
            df.to_csv('nelson_forecast_weather.csv', index=False)
            print('Weather forecast data has been saved as nelson_forecast_weather.csv')
        else:
            print(f'Request fail, states code: {forecast_response.status_code}')
    except Exception as e:
        print("This is error message: ", e)

def send_message(message):
    try:
        result = jsn.store(config.chat_table, [message])
        return result
    except Exception as e:
        print("This is error message: ", e)
        return None
    
def get_chat_data():
    try:
        chat_result = jsn.all(config.chat_table)
        if chat_result:
            formatted_messages_list = []
            for i in chat_result:
                formatted_message = f"User: {i["UserID"]}: \n Message: {i["Message"]} \n {'-' * 30}"
                formatted_messages_list.append(formatted_message)                
        return "\n".join(formatted_messages_list)
    except Exception as e:
        print("This is error message: ", e)