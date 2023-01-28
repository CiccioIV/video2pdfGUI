import PySimpleGUI as sg
import video2pdfslides as v2pfd
from pathlib import Path

layout = [
            [sg.Text('Video2pdf GUI')],
            [sg.FileBrowse('Pick a file',
             tooltip='Select the file which you wanty to get the slides from',
             key='-BTNFILE-', target='-TXTFILETOCONVERT-',
             enable_events=True)],
             [sg.Input('', key='-TXTFILETOCONVERT-', readonly=True,            enable_events=True, text_color='black',
                disabled_readonly_background_color=sg.theme_background_color(),
                expand_x=True)],
             [sg.FolderBrowse('Save to', 
                tooltip='Select a folder where to save the outputs',
                 key='-BTNSAVEFOLDER-', target='-TXTSAVEFOLDER-',
                 enable_events=True)],
             [sg.Input('', key='-TXTSAVEFOLDER-', 
             readonly=True, enable_events=True, text_color='black',
             disabled_readonly_background_color=sg.theme_background_color(),
             expand_x=True)],
             [sg.Button('CONVERT', key='-BTNCONVERT-', size=(10,2),
             disabled=True, tooltip='Start the conversion')],
         ]

window = sg.Window('Video2Pdf GUI', layout, size=(400,300))


# MAIN WINDOW LOOP
while True:
    event, values = window.read()
    print(event, values)

    # input file event
    if event == "-BTNFILE-" or event == '-TXTFILETOCONVERT-':
        if values['-BTNFILE-'] != "":
            window['-TXTFILETOCONVERT-'].set_tooltip(values['-BTNFILE-'])
        else:
            window['-TXTFILETOCONVERT-'].set_tooltip('no file selected')

    # select folder browse event
    if event == '-BTNSAVEFOLDER-' or event == '-TXTSAVEFOLDER-':
        if values['-BTNSAVEFOLDER-'] != "":
            window['-TXTSAVEFOLDER-'].set_tooltip(values['-BTNSAVEFOLDER-'])
    else:
            window['-TXTSAVEFOLDER-'].set_tooltip('no file selected')

    # Enable convert button if all data are provided
    if values['-BTNFILE-'] != "" and values['-BTNSAVEFOLDER-'] != "":
        window['-BTNCONVERT-'].update(disabled=False)
    else:
        window['-BTNCONVERT-'].update(disabled=True)

    # convert button event
    if event == '-BTNCONVERT-':
        sg.Popup('starting the process')
    

    # window close
    if event == sg.WIN_CLOSED:
        break

window.close()