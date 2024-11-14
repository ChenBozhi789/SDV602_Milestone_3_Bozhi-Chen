import PySimpleGUI as sg

def make_DES(title, cmd_text):
    """
    Make a generic DES window

    Args:
        title (str): The title for the DES window.
        cmd_text (str): The placeholder text for the input field.
        get_weather_data (function): Function to get data for this DES screen.
        draw_function (function): Function to draw the figure for this DES screen.

    Returns:
        sg.Window: The DES window object
    """
    sg.theme('BrownBlue')
    figure_w = 600
    figure_h = 400

    title_row = [
        [sg.Push(),
        sg.Text(title, justification='center', size=(10, 1), font=('Calibri Light', 24, 'bold')),
        sg.Push(),
        sg.Text('', justification='center', size=(50, 1), font=('Calibri Light', 12, 'bold'), key='-CMDOUTPUT-'),
        sg.Input(key='-IN-', size=(50, 5), default_text=cmd_text, enable_events=True),
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
         sg.Button('ZOOM IN', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-ZOOM_IN-'),
         sg.Button('ZOOM OUT', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-ZOOM_OUT-'),
         sg.Button('GET CURRENT DATA', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-GET_CURRENT-'),
         sg.Button('GET FORECAST DATA', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-GET_FORECAST-')]
    ]

    layout = [
        [title_row],
        [sg.Column([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]]), sg.Column(multiline_element)],
        [button_element]
    ]

    return sg.Window(title, layout, size=(1500, 800), finalize=True)