import PySimpleGUI as sg
import video2pdfslides as v2pfd
from pathlib import Path
from threading import Thread
import concurrent.futures

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
             [sg.Button('Get Picks', key='-BTNGETPICS-', size=(10,2),
             disabled=True, tooltip='Start the 1st step, getting pics fro video file')],
             [sg.Button('MERGE PICS', tooltip="Start the 2nd process, merging all pics in one .pdf file", size=(10,2),enable_events=True, disabled=True, key='-BTNMERGE-')],
             [sg.Output(size=(400,400))],
         ]

window = sg.Window('Video2Pdf GUI', layout, size=(600,500))


# MAIN WINDOW LOOP
while True:
    event, values = window.read(timeout=10)
    # print(event, values)

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
        window['-BTNGETPICS-'].update(disabled=False)
    else:
        window['-BTNGETPICS-'].update(disabled=True)

    # merge pics button event
    if event == '-BTNGETPICS-':
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                 fn = executor.submit(v2pfd.detect_unique_screenshots, values['-BTNFILE-'], values['-BTNSAVEFOLDER-'])
                 res = fn.result()
                 
            print(f"captured screenshots: {res}")
            # enable merge button if pics created
            if int(res) >0:
                sg.Popup(f'{res} pics returned.\nPlease open {values["-BTNSAVEFOLDER-"]}folder, delete unwanted pics, and hit "MERGE" button.')
                window['-BTNMERGE-'].update(disabled=False)
            else:
                window['-BTNMERGE-'].update(disabled=True)
        except Exception as e:
            print(e)
        
    if event == '-BTNMERGE-':
        try:
            v2pfd.convert_screenshots_to_pdf(values['-BTNSAVEFOLDER-'], values['-BTNFILE-'])
            sg.Popup('Conversion ended')
        except Exception as e:
            print(e)
        
    

    # window close
    if event == sg.WIN_CLOSED:
        break

window.close()