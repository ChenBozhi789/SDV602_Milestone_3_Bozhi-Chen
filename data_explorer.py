import config
import controller
import data
import network
import network.jsn_drop_service
import pandas as pd
import plot
import PySimpleGUI as sg
import views

def main():
    # Instantiate jsnDrop class
    jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)

    # Initialize remote database
    data.data_manager.initialize_database()

    registration_window = views.make_registration_window()

    while True:
        # Read all windows
        window, event, values = sg.read_all_windows()
        
        # Button event handle
        if event == sg.WIN_CLOSED or event == '-EXIT-' or event == 'Exit':
            break
        elif event == 'Register':
            try:
                config.register_id = values['-REG_USER-']
                config.register_pwd = values['-REG_PWD-']
                value_list = [{"UserID":config.register_id, "Pwd":config.register_pwd}]
                
                # Check if this user exists
                check_user_result = data.data_manager.get_user_data()
                if check_user_result == "Data error. Nothing selected from tbUser":
                    jsn.store(config.user_table, value_list)
                    print("Congrats! Register account successfully!")
                    login_window = views.make_login_window()
                    registration_window.close()
                else:
                    print("Register user fail")
            except Exception as e:
                print("Error: ", e)
        elif event == '-LOGIN-':
            config.login_id = values['-LOG_USER-']
            config.login_pwd = values['-LOG_PWD-']
            where_clause = f"UserID = {config.login_id} AND Pwd = {config.login_pwd}"

            select_result = jsn.select(config.user_table, where_clause)

            if select_result == "Data error. Nothing selected from tbUser":
                invalid_message = 'Invalid credentials, please check again'
                login_window['-LOG_OUTPUT-'].update(invalid_message)
            else:
                config.list_of_window_references[config.current_window] = controller.make_DES("DES_One", "This is input area")
                config.list_of_window_references[config.current_window].UnHide()
                config.current_user = values["-LOG_USER-"]

                config.fig, config.ax1 = plot.chart.print_placeholder()
                config.figure_agg = plot.draw_figure(config.list_of_window_references[config.current_window]['-CANVAS-'].TKCanvas, config.fig)
                chat_data = data.data_manager.get_chat_data()
                config.list_of_window_references[config.current_window]["-CHAT-AREA-"].update(chat_data)
                login_window.close()       
        elif event == '-OPEN_REG-':
            registration_window = views.make_registration_window()
            login_window.close()                         
        elif event == '-OPEN_LOGIN-':
            login_window = views.make_login_window()
            registration_window.close()
        elif event == '-PREVIOUS-' or event == '-NEXT-':
            # Hide current DES window
            if config.current_window in config.list_of_window_references:
                config.list_of_window_references[config.current_window].Hide()
            if event == '-NEXT-':
                config.current_window += 1
                # When current_window up to 3
                if config.current_window >= config.max_windows:
                    config.current_window = 0
            else:
                config.current_window -= 1
                if config.current_window < 0:
                    config.current_window = config.max_windows - 1
            # If this DES screen doesn't exist
            if  config.current_window not in config.list_of_window_references:
                if config.current_window == 0:
                    config.list_of_window_references[0] = controller.make_DES("DES_One", "This is input area")
                if config.current_window == 1:
                    config.list_of_window_references[1] = controller.make_DES("DES_Two", "This is input area")
                if config.current_window == 2:
                    config.list_of_window_references[2] = controller.make_DES("DES_Three", "This is input area")            
            config.list_of_window_references[config.current_window].UnHide()
        # Upload local file and display different graph
        elif event == '-LOAD_LOCAL_DATA-':            
            file_path = data.load_local_data()
            if file_path:
                config.original_file_path = file_path
                # Clear exists plot
                if config.figure_agg is not None:
                    plot.delete_figure_agg(config.figure_agg)

                # plot.delete_figure_agg(config.figure_agg)
                result = plot.draw_local_graph(file_path)
                # Check the number of result (Bar plot or line plot)
                if len(result) == 3:
                    config.fig, config.ax1, config.ax2 = result
                else:
                    config.fig, config.ax1 = result
                    config.ax2 = None
                config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)
            else:
                print("Invalid file path, please choose valid file path")
        elif event == '-MERGE-':
            if not config.original_file_path:
                print("Please upload a original local data first")
                continue
            merge_file_path = data.data_manager.load_local_data()
            if merge_file_path:
                # Clear exists plot
                if config.figure_agg is not None:
                    plot.delete_figure_agg(config.figure_agg)

                result = plot.draw_merge_graph(config.original_file_path, merge_file_path)
                try:
                    config.fig, config.ax1 = result
                    config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)
                except Exception as e:
                    config.fig, config.ax1 = plot.chart.print_placeholder()
                    config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)
                    print("This is error message: ", e)
        elif event == '-DRAW_REMOTE_CURRENT-':
            if config.figure_agg is not None:
                plot.delete_figure_agg(config.figure_agg)

            current_result = plot.chart.draw_current_data_from_remote(data.data_manager.get_current_weather_data())
            if current_result == None:
                print("Remote database doesn't have any data, please get data to remote first")
            else:
                config.fig, config.ax1 = current_result
                config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)
        elif event == '-DRAW_REMOTE_FORECAST-':
            if config.figure_agg is not None:
                plot.delete_figure_agg(config.figure_agg)

            forecast_result = plot.chart.draw_forecast_data_from_remote(data.data_manager.get_forecast_weather_data())
            if forecast_result == None:
                print("Remote database doesn't have any data, please get data to remote first")
            else:
                config.fig, config.ax1 = forecast_result
                config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)
        # Get data from API and upload to remote database
        elif event == '-UPLOAD_DATA_TO_REMOTE-':
            data.data_manager.upload_data_to_remote()
        # Upload local current data to remote database    
        elif event == '-UPLOAD_LOCAL_CURRENT-':
            upload_current_data = data.data_manager.load_local_data()
            if upload_current_data:
                current_data = pd.read_csv(upload_current_data)
                data.data_manager.upload_current_data_to_remote(current_data)
        # Upload local forecast data to remote database    
        elif event == '-UPLOAD_LOCAL_FORECAST-':
            upload_remote_data = data.data_manager.load_local_data()
            if upload_remote_data:
                forecast_data = pd.read_csv(upload_remote_data)
                data.data_manager.upload_forecast_data_to_remote(forecast_data)
        # Draw remote current merge data plot
        elif event == '-DRAW_MERGE_CURRENT-':
            if config.figure_agg is not None:
                plot.delete_figure_agg(config.figure_agg)

            result = plot.chart.draw_current_data_from_remote(data.data_manager.get_current_weather_data())
            if result:
                config.fig, config.ax1 = result
                config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)       
        # Draw remote forecast merge data plot         
        elif event == '-DRAW_MERGE_FORECAST-':
            if config.figure_agg is not None:
                plot.delete_figure_agg(config.figure_agg)

            result = plot.chart.draw_forecast_data_from_remote(data.data_manager.get_forecast_weather_data())
            if result:
                config.fig, config.ax1 = result
                config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)
        elif event == '-SEND-':
            message = {
                    "UserID": config.current_user,
                    "Message": values["-CHAT-"]
                }
            data.data_manager.send_message(message)
            chat_data = data.data_manager.get_chat_data()
            window["-CHAT-AREA-"].update(chat_data)
            window["-CHAT-"].update("")
        # Refresh chat display
        elif event == '-REFRESH-':
            chat_data = data.data_manager.get_chat_data()
            window["-CHAT-AREA-"].update(chat_data)
        elif event == '-ZOOM_IN-':
            if config.ax2:
                plot.zoom_in(config.ax1, config.ax2)
            else:
                plot.zoom_in(config.ax1)
        elif event == '-ZOOM_OUT-':
            if config.ax2:
                plot.zoom_out(config.ax1, config.ax2)
            else:
                plot.zoom_out(config.ax1)
        # Get API data and download as csv file in local computer
        elif event == '-DOWNLOAD-':
            data.data_manager.download_data_as_csv()
    window.close()

if __name__ == "__main__":
    main()