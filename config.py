# DES variable
current_window = 0
max_windows = 3
list_of_window_references = {}
figure_agg = None

# matplotlib variable
fig, ax1, ax2 = None, None, None
scale_factor = 1.2

# data variable
API_KEY = '2a86ef82b86f547e5b33df59dea5b840'
lat = '-41.270634'
lon = '173.283966'
url_current = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'
url_forecast = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}'

register_id = None
register_pwd = None
login_id = None
login_pwd = None
current_user = None

original_file_path = None

token = '9401b558-386d-48cb-ab8d-c2b418239ae7'
url = 'https://newsimland.com/~todd/JSON/'

user_table = 'tbUser'
current_data_table = 'tbCurrentData'
forecast_data_table = 'tbForecastData'
chat_table = 'tbChat'

tbUser_example = {"UserID PK":"UserID", "Pwd":"Password"}
tbCurrentData_example = {"City PK": "CURRENT_CITY_NAME","Temperature":"TEMPERATURE","Humidity":"HUMIDITY","Wind Speed":"WIND_SPEED_ALL_INFORMATION","Cloud info":"CLOUD_ALL_INFORMATION"}
tbForecastData_example = {"Date PK": "THE_CURRENT_TIME_YY_MM_DD","Temperature": "TEMPERATURE"}
tbChat_example = {"UserID": "THIS_USER_ID","Message": "THE_MESSAGE_CONTENT_YOU_CAN_TYPE_WHAT_EVER_YOU_WANT"}