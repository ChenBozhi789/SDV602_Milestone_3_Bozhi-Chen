import requests
import pandas as pd

API_KEY = '2a86ef82b86f547e5b33df59dea5b840'
lat = '-41.270634'
lon = '173.283966'

# Call current weather data
url_current = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
# Call 5 day / 3 hour forecast data
url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}'


# Get current weather data and save as csv file
# current_response = requests.get(url_current)

# if current_response.status_code == 200:
#     # Parse data to json file
#     current_data = current_response.json()
#     weather_data = {
#         'City': current_data['name'],
#         'Temperature (°C)': round(current_data['main']['temp'] - 273.15, 2),
#         'Humidity (%)': current_data['main']['humidity'],
#         'Wind Speed (m/s)': current_data['wind']['speed'],
#         'Cloud info': current_data["clouds"]["all"]
#     }

#     df = pd.DataFrame([weather_data])
#     df.to_csv('nelson_weather.csv', index=False)
#     print('Weather current data has been saved as nelson_weather.csv')
# else:
#     print(f'Request fail, states code: {current_response.status_code}')

# # Get forecast weather data and save as csv file
forecast_response = requests.get(url_forecast)

if forecast_response.status_code == 200:
    forecast_data = forecast_response.json()
    forecast_weather_list = []

    for i in forecast_data['list'][:8]:
        # Parse data to json file
        weather_data = {    
            'Time': i['dt_txt'],
            'Temperature (°C)': round(i["main"]["temp"] - 273.15, 2)
        }
        forecast_weather_list.append(weather_data)

    df = pd.DataFrame(forecast_weather_list)
    df.to_csv('nelson_forecast_weather.csv', index=False)
    print('Weather forecast data has been saved as nelson_forecast_weather.csv')
else:
    print(f'Request fail, states code: {forecast_response.status_code}')