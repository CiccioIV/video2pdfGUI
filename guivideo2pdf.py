import PySimpleGUI as sg
import video2pdfslides as v2pfd
import concurrent.futures
import img.icons

# set tooltips
tip_framerate = 'no.of frames per second that needs to be processed, fewer the count faster the speed.'
tip_warmup = 'initial number of frames to be skipped'
tip_sliderminpct = 'min % of difference between foreground and background to detect if motion has stopped'
tip_slidermaxpct = 'max % of difference between foreground and background to detect if frame is still in motion'
tip_threshold = 'Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model.'
tip_detectshadows = 'If true, the algorithm will detect shadows and mark them.'


# layouts
option_col1 = [
                [sg.Text('Frame rate')],
                [sg.Slider(range=(1,50), default_value=3, orientation='h', enable_events=True, key='-SLIDERFRAMERATE-', tooltip=tip_framerate)],
                [sg.Text('Warmup')],
                [sg.Slider(range=(1,50), default_value=3, orientation='h', enable_events=True, key='-SLIDERWARMUP-', tooltip=tip_warmup)],
              ]

option_col2 = [
                [sg.Text('Min/Max percent')],
                [sg.Slider(range=(0.1,5.0), default_value=0.1, orientation='h', enable_events=True, key='-SLIDERMINPCT-', tooltip=tip_sliderminpct,resolution=0.1)],
                [sg.Slider(range=(0.1,5.0), default_value=3, orientation='h', enable_events=True, key='-SLIDERMAXPCT-', tooltip=tip_slidermaxpct, resolution=0.1)],
              ]

option_col3 = [
                [sg.Text('Threshold')],
                [sg.Slider(range=(1,50), default_value=16, orientation='h', enable_events=True, key='-SLIDERTHRESHOLD-', tooltip=tip_threshold)],
                [sg.Checkbox('Detect Shadows', default=False, key='-CKBOXSHADOWS-', tooltip=tip_detectshadows, enable_events=True)],

              ]

options_frame = [
                    [sg.Column(option_col1),
                    sg.VerticalSeparator(),
                    sg.Column(option_col2),
                    sg.VerticalSeparator(),               
                    sg.Column(option_col3)],    
                ]

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
             [sg.Frame('options', title_color='red', layout=options_frame)],
             [sg.Button('Show internal options', key='-BTNGETOPT-', enable_events=True, tooltip='Show the current set options')],
             [sg.Button('Get Picks', key='-BTNGETPICS-', size=(10,2),
             disabled=True, tooltip='Start the 1st step, getting pics fro video file')],
             [sg.Button('MERGE PICS', tooltip="Start the 2nd process, merging all pics in one .pdf file", size=(10,2),enable_events=True, disabled=True, key='-BTNMERGE-')],
             [sg.Output(size=(400,400), key='-OUT-')],
          ]


# Functions
def get_current_settings():
    vars = [v2pfd.FRAME_RATE, v2pfd.WARMUP, v2pfd.FGBG_HISTORY, v2pfd.VAR_THRESHOLD, v2pfd.DETECT_SHADOWS, v2pfd.MIN_PERCENT, v2pfd.MAX_PERCENT]

    return f"framerate:{v2pfd.FRAME_RATE}\nwarmup:{v2pfd.WARMUP}\nfgbg history:{v2pfd.FGBG_HISTORY}\nthreshold:{v2pfd.VAR_THRESHOLD}\ndetect shadows:{v2pfd.DETECT_SHADOWS}\nmin%:{v2pfd.MIN_PERCENT}\nmax%{v2pfd.MAX_PERCENT}"
         

window = sg.Window('Video2Pdf GUI', layout,size=(600,500), icon=img.icons.ICON1)


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

    # set options
    if event == '-SLIDERFRAMERATE-':
        v2pfd.FRAME_RATE = values['-SLIDERFRAMERATE-']
        # set fgbg according to framerate
        v2pfd.FGBG_HISTORY = values['-SLIDERFRAMERATE-']*15
        # if framerate is updated, syncs the warmup slider as well
        # need to find out how to move the slider actually
        window['-SLIDERWARMUP-'].update(value=values['-SLIDERFRAMERATE-'])
        v2pfd.WARMUP = values['-SLIDERFRAMERATE-']
        window.refresh()
    if event == '-SLIDERWARMUP-':
        v2pfd.WARMUP = values['-SLIDERWARMUP-']
    if event == '-SLIDERMINPCT-':
        v2pfd.MIN_PERCENT = values['-SLIDERMINPCT-']
    if event == '-SLIDERMAXPCT-':
        v2pfd.MAX_PERCENT = values['-SLIDERMAXPCT-']
    if event == '-SLIDERTHRESHOLD-':
        v2pfd.VAR_THRESHOLD = values['-SLIDERTHRESHOLD-']
    if event == '-CKBOXSHADOWS-':
        v2pfd.DETECT_SHADOWS = values['-CKBOXSHADOWS-']

    try:
        if event == '-BTNGETOPT-':
            window['-OUT-'].update('')
            sg.Popup(get_current_settings())
    except Exception as e:
        sg.Popup(e)


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