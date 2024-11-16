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
    try:
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
            [sg.Multiline(size=(45, 32), justification='left', font=('Calibri', 12, 'bold'), key='-CHAT-AREA-', disabled=True)]
        ]   

        button_element = [
            [sg.Button('LOAD LOCAL DATA', font=('Calibri Light', 12, 'bold'), size=(10, 3), key='-LOAD_LOCAL_DATA-'),
            sg.Button('MERGE LOCAL DATA', font=('Calibri Light', 12, 'bold'), size=(15, 3), key='-MERGE-'),
            sg.Button('DRAW REMOTE \n CURRENT DATA', font=('Calibri Light', 12, 'bold'), size=(15, 3), key='-DRAW_REMOTE_CURRENT-'),
            sg.Button('DRAW REMOTE \n FORECAST DATA', font=('Calibri Light', 12, 'bold'), size=(15, 3), key='-DRAW_REMOTE_FORECAST-'),
            sg.Button('UPLOAD DATA TO REMOTE', font=('Calibri Light', 12, 'bold'), size=(10, 3), key='-UPLOAD_DATA_TO_REMOTE-'),
            sg.Button('UPLOAD LOCAL \n CURRENT DATA \n TO REMOTE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-UPLOAD_LOCAL_CURRENT-'),
            sg.Button('UPLOAD LOCAL \n FORECAST DATA TO \n REMOTE', font=('Calibri Light', 12, 'bold'), size=(20, 3), key='-UPLOAD_LOCAL_FORECAST-'),            
            sg.Button('DRAW REMOTE \n CURRENT \n MERGE DATA', font=('Calibri Light', 12, 'bold'), size=(15, 3), key='-DRAW_MERGE_CURRENT-'),
            sg.Button('DRAW REMOTE \n FORECAST \n MERGE DATA', font=('Calibri Light', 12, 'bold'), size=(15, 3), key='-DRAW_MERGE_FORECAST-')]
        ]

        layout = [
            [title_row],
            [sg.Column([[sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')]]), sg.Column(multiline_element)],
            [button_element],
            [sg.Input(key='-CHAT-', size=(50, 0), font=('Calibri Light', 12, 'bold'), enable_events=True),
            sg.Button('SEND', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-SEND-'),
            sg.Button('REFRESH', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-REFRESH-'),
            sg.Button('ZOOM IN', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-ZOOM_IN-'),
            sg.Button('ZOOM OUT', font=('Calibri Light', 12, 'bold'), size=(10, 0), key='-ZOOM_OUT-'),
            sg.Button('DOWNLOAD DATA TO LOCAL', font=('Calibri Light', 12, 'bold'), size=(25, 0), key='-DOWNLOAD-')]
        ]

        return sg.Window(title, layout, size=(1400, 800), finalize=True)
    except Exception as e:
        print("This is error message: ", e)