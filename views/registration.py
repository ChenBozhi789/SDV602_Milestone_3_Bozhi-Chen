import PySimpleGUI as sg

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
        [sg.Button('Register', size=(10, 0), pad=((140, 0), (5, 0)), font=('Helvetica', 12)), sg.Button('Exit', size=(5, 0), pad=((80, 0), (5, 0)), font=('Helvetica', 12))]
    ]
    return sg.Window('Registration', layout, size=(400, 200), finalize=True)