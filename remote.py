import config 
import data
from datetime import datetime
import network.jsn_drop_service




# def test_store_weather():
#     """测试函数：获取天气数据并存储到tbData表"""
    
#     try:
#         # 1. 获取当前天气数据
#         current_data, _ = data.get_weather_data()
        
#         if current_data:
#             # 2. 按照tbData表的格式整理数据
#             formatted_data = {
#                 "Date": current_data["dt"],
#                 "temperature": round(current_data["main"]["temp"] - 273.15, 2),  # 转换为摄氏度
#                 "humidity": current_data["main"]["humidity"],
#                 "description": current_data["weather"][0]["description"]
#             }
            
#             # 3. 创建JSnDrop实例并存储数据
#             jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)
#             store_result = jsn.store("tbData", [formatted_data])  # 注意这里表名是"tbData"
            
#             print("Formatted data being sent:", formatted_data)  # 打印要发送的数据
#             print("Store result:", store_result)  # 打印存储结果
            
#             return store_result
            
#     except Exception as e:
#         print(f"Error in test_store_weather: {str(e)}")
#         return False

def store_foreast_to_remote():
    try:
        current_data, forecast_data = data.get_weather_data()
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
            print("Data stored successfully!")
            return True
        else:
            print("Failed to store data!")
            return False
    except Exception as e:
        print("Error: ", e)

# 运行测试
if __name__ == "__main__":
    print("Starting weather data storage test...")
    success = store_foreast_to_remote()
    print(success)