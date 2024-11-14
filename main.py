import config
import controller
import data
import network
import network.jsn_drop_service
import plot
import PySimpleGUI as sg
import views

def main():
    # Get weather data
    

    # window = controller.make_DES("DES_Tester_ONE", "This is input area")

    # fig = plot.draw_current_temperature(weather_data)
    # figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, fig)

    # Instantiate jsnDrop class
    jsn = network.jsn_drop_service.jsnDrop(config.token, config.url)

    # Initialize remote database
    data.data_manager.initialize_database()
    current_data, forecast_data = data.get_weather_data()

    registration_window = views.make_registration_window()

    while True:
        # Read all windows
        window, event, values = sg.read_all_windows()
        
        # Button event handle
        if event == sg.WIN_CLOSED or event == '-EXIT-' or event == 'Exit':
            break
        elif event == 'Register':
            try:
                register_id = values['-REG_USER-']
                register_pwd = values['-REG_PWD-']
                value_list = [{"UserID":register_id, "Pwd":register_pwd}]
                
                # Check if this user exists
                check_user_result = jsn.select(config.user_table, register_id)
                if check_user_result == "Data error. Nothing selected from tbUser":
                    jsn.store(config.user_table, value_list)
                    login_window = views.make_login_window()
                    registration_window.close()
                else:
                    print("Register user fail")
            except Exception as e:
                print("Error: ", e)
        elif event == '-OPEN_LOGIN-':
            login_window = views.make_login_window()
            registration_window.close()
        elif event == '-OPEN_REG-':
            registration_window = views.make_registration_window()
            login_window.close()
        elif event == '-LOGIN-':
            login_id = values['-LOG_USER-']
            login_pwd = values['-LOG_PWD-']
            where_clause = f"UserID = {login_id} AND Pwd = {login_pwd}"

            select_result = jsn.select(config.user_table, where_clause)

            if select_result == "Data error. Nothing selected from tbUser":
                invalid_message = 'Invalid credentials, please check again'
                login_window['-LOG_OUTPUT-'].update(invalid_message)
            else:
                config.list_of_window_references[config.current_window] = controller.make_DES("DES_One", "This is input area")
                config.list_of_window_references[config.current_window].UnHide()
                login_window.close()
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
        elif event == '-SET_DATA_SOURCE-':
            print("You just clicked 'Set data source' button")
        # Upload local file and display different graph
        elif event == '-UPLOAD_DATA_SOURCE-':            
            file_path = data.load_local_data()
            if file_path:
                if config.figure_agg is not None:
                    plot.delete_figure_agg(config.figure_agg)

                # plot.delete_figure_agg(config.figure_agg)
                result = plot.draw_local_graph(file_path)
                # Check the number of result (Bar plot or line plot)
                # Bar plot
                if len(result) == 3:
                    config.fig, config.ax1, config.ax2 = result
                # Line plot
                else:
                    config.fig, config.ax1 = result
                    config.ax2 = None
                config.figure_agg = plot.draw_figure(window['-CANVAS-'].TKCanvas, config.fig)
            else:
                print("Invalid file path, please choose valid file path")
        elif event == '-SETTINGE-':
            print("You just clicked 'SETTING' button")
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
        elif event == '-GET_CURRENT-':
            data.data_manager.store_current_to_remote()
        elif event == '-GET_FORECAST-':
            data.data_manager.store_forecast_to_remote()

    window.close()

if __name__ == "__main__":
    main()
