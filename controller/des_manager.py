import config
from . import DES

def show_current_window():
    for i in range(0, config.max_windows):
        # If i not equal to index of current window
        if i in config.list_of_window_references and i != config.current_window:
            config.list_of_window_references[i].Hide()

        if i in config.list_of_window_references:
            config.list_of_window_references[config.current_window].UnHide()

def handle_input(command):
    command = command.lower().strip()
    if command == 'des_one':        
        config.current_window = 0
        show_current_window()
    elif command == 'des_two':
        config.current_window = 1
        if config.current_window not in config.list_of_window_references:
            config.list_of_window_references[1] = DES.make_DES()
        show_current_window()
    elif command == 'des_three':
        config.current_window = 2
        if config.current_window not in config.list_of_window_references:
            config.list_of_window_references[2] = DES.make_DES()
        show_current_window()
    else:
        config.list_of_window_references[config.current_window]['-CMDOUTPUT-'].update('Supported Commands: des_one, des_two or des_three')