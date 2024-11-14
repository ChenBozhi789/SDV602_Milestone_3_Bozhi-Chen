# DES variable
current_window = 0
max_windows = 3
list_of_window_references = {}
figure_agg = None

# matplotlib variable
fig, ax1, ax2 = None, None, None
scale_factor = 1.2

# data variable
token = '9401b558-386d-48cb-ab8d-c2b418239ae7'
url = 'https://newsimland.com/~todd/JSON/'
user_table = 'tbUser'
current_data_table = 'tbCurrentData'
forecast_data_table = 'tbForecastData'
chat_table = 'tbChat'
tbUser_example = {"UserID PK":"tbUser", "Pwd":"Password"}
tbCurrentData_example = {"Date PK": "THE_CURRENT_TIME_YY_MM_DD","Temperature": "TEMPERATURE","Humidity": "HUMIDITY","Description": "THIS_IS_WEATHER_DESCRIPTION_TEXT"}
tbForecastData_example = {"Date PK": "THE_CURRENT_TIME_YY_MM_DD","Temperature": "TEMPERATURE"}