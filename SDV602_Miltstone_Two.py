import json
import os
import PySimpleGUI as sg
import weather_matplotlib as mt
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Data file for storing user data
DATA_FILE = 'data.json'

current_window = 0
max_windows = 3
list_of_window_references = {}
figure_agg = None

def draw_figure(canvas, figure):
    """
    Draw a Matplotlib figure on a Tkinter Canvas.

    Args:
        canvas (Tk.Canvas): The Tkinter canvas to draw on.
        figure (FigureCanvasTkAgg): The Matplotlib figure object to be drawn.

    Returns:
        FigureCanvasTkAgg: The figure canvas object that allows further manipulation.
    """
    # Convert Matplotlib figure (i.e., a chart object) to FigureCanvasTkAgg object
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    # Drawing chart
    figure_canvas_agg.draw()
    # Place a Matplotlib chart in a Tkinter window and control how it is laid out.
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)  
    return figure_canvas_agg

# Need explanation
def delete_figure_agg(figure_agg):
    """
    Close and delete all Matplotlib figures.

    Args:
        figure_agg (FigureCanvasTkAgg): The figure canvas object to close and delete.

    Returns:
        None
    """
    plt.pyplot.close('all')

def load_date():
    """
    Load data from data.json file

    Returns:
        dict: The data from the data.json file.
        If data doesn't exists, returns empty dict
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file) # If the file exists, return the data
    return {} # If the file doesn't exist, return an empty dictionary

    # try ... except

def save_data(data):
    """
    Save data into data.json file

    Args:
        data (dict): The data to be saved into the data.json file

    Returns:
        bool: Returns True if the data is successfully saved, False otherwise.
    """
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4) # Save the data into the data.json file
    except OSError:
        print('File is not exists')
        return False

def user_register(username, password):
    """
    Register a user into the data.json file
    
    Args:
        username (str): The username of the user
        password (str): The password of the user

    Returns:
        bool: Returns true if the user is registered, False otherwise
    """
    global registration_window
    # Load the data from the data.json file
    data = load_date() 

    # If user already exists, return False
    if username in data:
        error_message = 'Username already exists, please try again'
        registration_window['-OUTPUT-'].update(error_message)
        return False
    # If user doesn't exist, add the user to the data
    else:
        data[username] = password
        save_data(data)
        return True

def user_login(username, password):
    """
    Login a user into the data.json file
    
    Args:
        username (str): The username of the user
        password (str): The password of the user

    Returns:
        bool: Returns true if the user is logged in, False otherwise
    """
    # Load the data from the data.json file
    data = load_date()
    # When username exists
    if username in data:
        # When username and password are correct
        if data[username] == password:
            return True
        # When username or password is incorrect
        else:            
            return False
    # When username does not exist
    else:
        return False

def make_registration_window():
    """
    Make the registration window

    Returns:
        sg.Window: The registration window object
    """
    sg.theme('BrownBlue')
    input_elements = [    
        [sg.Text('Username', font=('Helvetica', 12, 'bold')), sg.Input(key='-REG_USER-', enable_events=True, size=(40, 1))],        
        [sg.Text('Password', font=('Helvetica', 12, 'bold')), sg.Input(key='-REG_PWD-', password_char='*', enable_events=True, size=(40, 1))],
    ]
    layout = [
        [sg.Text('Registration', justification='center', size=(500, 1), font=('Calibri Light', 12, 'bold'))],
        [input_elements],
        # [sg.Button('Already have an account? Login', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0, key='-OPEN_LOGIN-', font=('Helvetica', 10, 'underline'))],
        [sg.Button('Already have an account? Click me to Login', button_color=('Blue', sg.theme_background_color()), border_width=0, key='-OPEN_LOGIN-', font=('Helvetica', 10, 'underline'))],
        [sg.Text('Please enter your username and password to register', font=('Calibri', 12, 'bold'), justification='center', key='-OUTPUT-')],
        [sg.Button('Register', size=(10, 0), pad=((140, 0), (5, 0)), font=('Helvetica', 12))]
    ]
    return sg.Window('Registration', layout, size=(400, 200), finalize=True)

def make_login_window():
    """
    Make the login window

    Returns:
        sg.Window: The login window object
    """
    sg.theme('BrownBlue')
    input_elements = [
        [sg.Text('Username', font=('Calibri', 12, 'bold')), sg.Input(key='-LOG_USER-', enable_events=True)],
        [sg.Text('Password', font=('Calibri', 12, 'bold')), sg.Input(key='-LOG_PWD-', password_char='*', enable_events=True)],
    ]

    layout = [
        [sg.Text('Login', justification='center', size=(500, 1), font=('Calibri Light', 12, 'bold'))],
        [input_elements],
        [sg.Button('Still no account?', button_color=('Blue', sg.theme_background_color()), border_width=0, key='-OPEN_REG-', font=('Helvetica', 10, 'underline'))],
        [sg.Button('Login', size=(10, 0), pad=((140, 0)), font=('Helvetica', 12), key='-LOGIN-')],        
        [sg.Text('Please enter your Username and Password',  pad=((10, 0), (5, 0)), font=('Helvetica', 12, 'bold'), justification='center', key='-LOG_OUTPUT-')]
    ]
    return sg.Window('Login', layout, size=(400, 200), finalize=True)

def make_DES_One():
    """
    Make the DES One window

    Returns:
        sg.Window: The DES window object
    """
    global figure_agg
    sg.theme('BrownBlue')
    figure_w = 600
    figure_h = 400

    title_row = [
        [sg.Push(),
        sg.Text("DES_ONE", justification='center', size=(8, 1), font=('Calibri Light', 24, 'bold')),
        sg.Push(),
        sg.Text('', justification='center', size=(50, 1), font=('Calibri Light', 12, 'bold'), key='-CMDOUTPUT-'),
        sg.Input(key='-IN-', size=(50, 5), default_text='Enter command: DES_One, DES_Two, or DES_Three', enable_events=True),
        sg.Button('Previous', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-PREVIOUS-'),
        sg.Button('Next', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-NEXT-')]
    ]
    
    multiline_element = [
        [sg.Multiline(size=(30, 38), justification='right', key='-SUMMARY-', disabled=True),
         sg.Multiline(size=(30, 38), justification='right', key='-CHAT-AREA-', disabled=True)]
    ]

    button_element = [
        [sg.Button('SET DATA SOURCE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-SET_DATA_SOURCE-'), 
         sg.Button('UPLOAD DATA SOURCE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-UPLOAD_DATA_SOURCE-'), 
         sg.Button('SETTING', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-SETTING-'),
         sg.Button('EXIT', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-EXIT-')]
    ]

    layout = [
        [title_row],
        [sg.Column([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]]), sg.Column(multiline_element)],
        [button_element]
    ]

    window = sg.Window('DES_One', layout, size=(1500, 800), finalize=True)
    
    # ** IMPORTANT ** Clean up previous drawing before drawing again
    if figure_agg:        
        delete_figure_agg(figure_agg)
        figure_agg = None
    
    # Getting current and forecast weather data
    current_data, forecast_data = mt.get_weather_data()
    fig = mt.draw_current_temperature(current_data)
    figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    return window

def make_DES_Two():
    """
    Make the DES Two window

    Returns:
        sg.Window: The DES window object
    """
    global figure_agg
    sg.theme('BrownBlue')
    figure_w = 600
    figure_h = 400

    title_row = [
        [sg.Push(),
        sg.Text("DES_TWO", justification='center', size=(8, 1), font=('Calibri Light', 24, 'bold')),
        sg.Push(),
        sg.Text('', justification='center', size=(50, 1), font=('Calibri Light', 12, 'bold'), key='-CMDOUTPUT-'),
        sg.Input(key='-IN-',  size=(50, 5), enable_events=True),
        sg.Button('Previous', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-PREVIOUS-'),
        sg.Button('Next', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-NEXT-')]
    ]
    
    multiline_element = [
        [sg.Multiline(size=(30, 38), justification='right', key='-SUMMARY-', disabled=True),
         sg.Multiline(size=(30, 38), justification='right', key='-CHAT-AREA-', disabled=True)]
    ]

    button_element = [
        [sg.Button('SET DATA SOURCE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-SET_DATA_SOURCE-'), 
         sg.Button('UPLOAD DATA SOURCE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-UPLOAD_DATA_SOURCE-'), 
         sg.Button('SETTING', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-SETTING-')]
    ]

    layout = [
        [title_row],
        [sg.Column([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]]), sg.Column(multiline_element)],
        [button_element]
    ]

    window2 = sg.Window('DES_Two', layout, size=(1500, 800), finalize=True)
    
    # ** IMPORTANT ** Clean up previous drawing before drawing again
    if figure_agg:        
        delete_figure_agg(figure_agg)
        figure_agg = None
    
    # Getting current and forecast weather data
    current_data, forecast_data = mt.get_weather_data()
    fig = mt.draw_forecast_temperature(forecast_data)
    figure_agg = draw_figure(window2['-CANVAS-'].TKCanvas, fig)

    return window2

def make_DES_Three():
    """
    Make the DES Three window

    Returns:
        sg.Window: The DES window object
    """
    global figure_agg
    sg.theme('BrownBlue')
    figure_w = 600
    figure_h = 400

    title_row = [
        [sg.Push(),
        sg.Text("DES_THREE", justification='center', size=(10, 1), font=('Calibri Light', 24, 'bold')),
        sg.Push(),
        sg.Text('', justification='center', size=(50, 1), font=('Calibri Light', 12, 'bold'), key='-CMDOUTPUT-'),
        sg.Input(key='-IN-', size=(50, 5), enable_events=True),
        sg.Button('Previous', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-PREVIOUS-'),
        sg.Button('Next', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-NEXT-')]
    ]
    
    multiline_element = [
        [sg.Multiline(size=(30, 38), justification='right', key='-SUMMARY-', disabled=True),
         sg.Multiline(size=(30, 38), justification='right', key='-CHAT-AREA-', disabled=True)]
    ]

    button_element = [
        [sg.Button('SET DATA SOURCE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-SET_DATA_SOURCE-'), 
         sg.Button('UPLOAD DATA SOURCE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-UPLOAD_DATA_SOURCE-'), 
         sg.Button('SETTING', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-SETTING-')]
    ]

    layout = [
        [title_row],
        [sg.Column([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]]), sg.Column(multiline_element)],
        [button_element]
    ]

    window3 = sg.Window('DES_Three', layout, size=(1500, 800), finalize=True)
    
    # ** IMPORTANT ** Clean up previous drawing before drawing again
    if figure_agg:        
        delete_figure_agg(figure_agg)
        figure_agg = None
    
    # Getting current and forecast weather data
    # current_data, forecast_data = mt.get_weather_data()
    fig = mt.print_placeholder()
    figure_agg = draw_figure(window3['-CANVAS-'].TKCanvas, fig)

    return window3

def show_current_window():
    for i in range(0, max_windows):
        # If i not equal to index of current window
        if  i in list_of_window_references and i != current_window:
            list_of_window_references[i].Hide()

        if i in list_of_window_references:
            list_of_window_references[current_window].UnHide()

def handle_input(command):
    global current_window
    command = command.lower().strip()
    if command == 'des_one':        
        current_window = 0
        show_current_window()
    elif command == 'des_two':
        current_window = 1
        if current_window not in list_of_window_references:
                list_of_window_references[1] = make_DES_Two()
        show_current_window()
    elif command == 'des_three':
        current_window = 2
        if current_window not in list_of_window_references:
                list_of_window_references[2] = make_DES_Three()
        show_current_window()
    else:
        list_of_window_references[current_window]['-CMDOUTPUT-'].update('Supported Commands: des_one, des_two or des_three')


def main():
    global current_window
    global registration_window
    
    registration_window = make_registration_window()
    while True:
        # Read all windows
        window, event, values = sg.read_all_windows() 
        if event == 'Register':
            input_username = values['-REG_USER-']
            input_password = values['-REG_PWD-']
            # When user register successfully
            if user_register(input_username, input_password):
                login_window = make_login_window()
                registration_window.close()
            else:
                pass
        # When user click the text label 'Already have an account? Login'
        elif event == '-OPEN_LOGIN-':
            login_window = make_login_window()
            registration_window.close()
        # When user click the login button
        elif event == '-OPEN_REG-':
            registration_window = make_registration_window()
            login_window.close()
        # When user click login button
        elif event == '-LOGIN-':
            input_username = values['-LOG_USER-']
            input_password = values['-LOG_PWD-']
            # When user login successfully (True)
            if user_login(input_username, input_password):                
                list_of_window_references[current_window] = make_DES_One()
                show_current_window()
                login_window.close()
            # When user login failed (False)
            else:
                invalid_message = 'Invalid username or password, please try again'
                login_window['-LOG_OUTPUT-'].update(invalid_message)
        elif event == '-PREVIOUS-' or event == '-NEXT-':
            if event == '-NEXT-':
                current_window += 1
                # When current_window up to 3
                if current_window >= max_windows:
                    current_window = 0
            else:
                current_window -= 1
                if current_window < 0:
                    current_window = max_windows - 1
            if current_window not in list_of_window_references:
                if current_window == 1:
                    list_of_window_references[1] = make_DES_Two()
                elif current_window == 2:
                    list_of_window_references[2] = make_DES_Three()
            show_current_window()
        elif event == '-IN-':
            command = values['-IN-']
            handle_input(command)
        elif event == '-SET_DATA_SOURCE-':
            pass
        elif event == '-UPLOAD_DATA_SOURCE-':
            pass
        elif event == '-SETTING-':
            pass
        # When user click the close button
        elif  event == sg.WIN_CLOSED or event == 'EXIT' or event is None: 
            break
        else:
            pass
    # registration_window.close()

if __name__ == "__main__":
    main()