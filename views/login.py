import PySimpleGUI as sg

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