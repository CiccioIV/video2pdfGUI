import PySimpleGUI as sg
import video2pdfslides as v2pdf
import concurrent.futures
import img.icons
import os

# set tooltips
tip_framerate = 'no.of frames per second that needs to be processed, fewer the count faster the speed.'
tip_warmup = 'initial number of frames to be skipped'
tip_bind_frate_wup = 'If the option is checked, setting the framerate will move the warmup bar as well.\nIf you want to set them separately, set the warmup AFTER the framerate, or uncheck this option to unbind them'
tip_fgbg_history = 'The number of frames history that effects the background subtractor\nCalculated over framerate value * 15'
tip_sliderminpct = 'min % of difference between foreground and background to detect if motion has stopped'
tip_slidermaxpct = 'max % of difference between foreground and background to detect if frame is still in motion'
tip_threshold = 'Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model.\nThis parameter does not affect the background update.'
tip_detectshadows = 'If true, the algorithm will detect shadows and mark them.\nIt decreases the speed a bit, so if you do not need this feature, set the parameter to false.'
tip_filebrowser = 'Select the file which you wanty to get the slides from'
tip_saveto = 'Select a folder where to save the outputs'
tip_show_i_opts = 'Show the current set options'
tip_getpics = 'Start the 1st step, getting pics from video file'
tip_mergepics = 'Start the 2nd process, merging all pics in one .pdf file'
tip_reset_defaults = 'Reset all core options to default values\nUse in case you messed up with options.\nApp options are unaffected by the reset'
tip_core_options_frame = 'These are the core options of the script.\nThey affects directly the conversion algorhytms.\nYou have to play with them if the conversion result does not matches with your expectations.'
tip_automerge = 'Check this option if you want to skip the 2nd step and automatically merge all the pics inside the output folder.\nThis is the quickest option to get final result, but the resulting file may have duplicated pics.'

APPICON = img.icons.ICON1
WINDOW_W = 800
WINDOW_H = 600


# layouts
core_option_col1 = [
                [sg.Text('Frame rate')],
                [sg.Slider(range=(1,50), default_value=3, orientation='h', 
                enable_events=True, key='-SLIDERFRAMERATE-', 
                tooltip=tip_framerate)],
                [sg.Text('Warmup')],
                [sg.Slider(range=(1,50), default_value=3, orientation='h',
                 enable_events=True, key='-SLIDERWARMUP-', 
                 tooltip=tip_warmup)],
                [sg.Checkbox('bind framerate/warmup', default=True,
                 tooltip=tip_bind_frate_wup, key='-CKBBINDFRATEWUP-', 
                 text_color='yellow')],
              ]

core_option_col2 = [
                [sg.Text('Min/Max percent')],
                [sg.Slider(range=(0.1,5.0), default_value=0.1, orientation='h', 
                enable_events=True, key='-SLIDERMINPCT-', 
                tooltip=tip_sliderminpct,resolution=0.1)],
                [sg.Slider(range=(0.1,5.0), default_value=3, orientation='h',
                 enable_events=True, key='-SLIDERMAXPCT-',
                 tooltip=tip_slidermaxpct, resolution=0.1)],
              ]

core_option_col3 = [
                [sg.Text('Threshold')],
                [sg.Slider(range=(1,50), default_value=16, orientation='h', 
                enable_events=True, key='-SLIDERTHRESHOLD-',
                tooltip=tip_threshold)],
                [sg.Checkbox('Detect Shadows', default=False,
                key='-CKBOXSHADOWS-', tooltip=tip_detectshadows,
                enable_events=True)],
                [sg.Text('FGBG history:'),
                 sg.Text('', key='-TXTHISTORY-', text_color='yellow')],

              ]

core_options_frame = [
                    [sg.Column(core_option_col1),
                    sg.VerticalSeparator(),
                    sg.Column(core_option_col2),
                    sg.VerticalSeparator(),               
                    sg.Column(core_option_col3)],    
                    [sg.Button('Show internal options', key='-BTNGETOPT-',
                     enable_events=True, tooltip=tip_show_i_opts),
                     sg.Button('reset to default', enable_events=True,
                     key='-BTNRESETDEFAULT-', tooltip=tip_reset_defaults)],
                ]


app_options_frame = [
                        [sg.Checkbox('auto merge', default=False,
                         key='-CKBAUTOMERGE-',
                         enable_events=True,
                         tooltip=tip_automerge)],
                    ]

layout = [
            [sg.FileBrowse('Pick a file',
             tooltip=tip_filebrowser,
             key='-BTNFILE-', target='-TXTFILETOCONVERT-',
             enable_events=True)],
             [sg.Input('', key='-TXTFILETOCONVERT-', readonly=True,
                enable_events=True, text_color='black',
                disabled_readonly_background_color=sg.theme_background_color(),
                expand_x=True)],
             [sg.FolderBrowse('Save to', 
                tooltip=tip_saveto,
                 key='-BTNSAVEFOLDER-', target='-TXTSAVEFOLDER-',
                 enable_events=True)],
             [sg.Input('', key='-TXTSAVEFOLDER-', 
             readonly=True, enable_events=True, text_color='black',
             disabled_readonly_background_color=sg.theme_background_color(),
             expand_x=True)],
             [sg.Frame('core options', title_color='red',
             layout=core_options_frame),
             sg.Frame('app options', app_options_frame)],
             [sg.Button('Get Pics', key='-BTNGETPICS-', size=(10,2),
             disabled=True, tooltip=tip_getpics),
             sg.Button('MERGE PICS', tooltip=tip_mergepics,
              size=(10,2),enable_events=True, 
              disabled=True, key='-BTNMERGE-')],
             [sg.Output(size=(WINDOW_W,10), key='-OUT-')],
          ]


# Functions
def get_current_settings():
    """Get the current global vars status from core module

    Returns:
        str: formatted string with vars values
    """
    return f"framerate:{v2pdf.FRAME_RATE}\nwarmup:{v2pdf.WARMUP}\nfgbg history:{v2pdf.FGBG_HISTORY}\nthreshold:{v2pdf.VAR_THRESHOLD}\ndetect shadows:{v2pdf.DETECT_SHADOWS}\nmin%:{v2pdf.MIN_PERCENT}\nmax%{v2pdf.MAX_PERCENT}"

def reset_defaults():
    """reset all option values to their defaults
    and updates the ui acccording
    """
    v2pdf.FRAME_RATE         = 3
    v2pdf.WARMUP             = 3
    v2pdf.MIN_PERCENT        = 0.1
    v2pdf.MAX_PERCENT        = 3
    v2pdf.VAR_THRESHOLD      = 16
    v2pdf.DETECT_SHADOWS     = False
    v2pdf.FGBG_HISTORY       = v2pdf.FRAME_RATE *15

    window['-SLIDERFRAMERATE-'].update(value=v2pdf.FRAME_RATE)
    window['-SLIDERWARMUP-'].update(value=v2pdf.WARMUP)
    window['-TXTHISTORY-'].update(value=v2pdf.FGBG_HISTORY)
    window['-SLIDERMINPCT-'].update(value=v2pdf.MIN_PERCENT)
    window['-SLIDERMAXPCT-'].update(value=v2pdf.MAX_PERCENT)
    window['-SLIDERTHRESHOLD-'].update(value=v2pdf.VAR_THRESHOLD)
    window['-CKBOXSHADOWS-'].update(value=v2pdf.DETECT_SHADOWS)
    window['-CKBBINDFRATEWUP-'].update(value=True)

    window.refresh()
    

def get_pics():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        fn = executor.submit(v2pdf.detect_unique_screenshots, 
                            values['-BTNFILE-'],
                                values['-BTNSAVEFOLDER-'])
        res = fn.result()
        
    print(f"captured screenshots: {res}")
    window.refresh()
    # enable merge button if pics created
    if int(res) >0:
        # calls 2nd step if automerge set to true
        if values['-CKBAUTOMERGE-']:
            print('auto merge set True. Auto merging pics')
            window.refresh()
            merge_pics() 
            return
        # otherwise ask user for 2nd step
        sg.Popup(f'{res} pics returned.\nClick "Ok" button here to open {values["-BTNSAVEFOLDER-"]}folder, delete duplicated or unwanted pics in the output folder, and then hit "MERGE" button in the main app window to merge all pics into pdf file.')
        os.startfile(fr'{values["-BTNSAVEFOLDER-"]}' ) #auto open output folder
        window['-BTNMERGE-'].update(disabled=False)
    else:
        window['-BTNMERGE-'].update(disabled=True)


def merge_pics():
    v2pdf.convert_screenshots_to_pdf(values['-BTNSAVEFOLDER-'],
                                    values['-BTNFILE-'])
    sg.Popup('Conversion ended')


window = sg.Window('Video2Pdf GUI',
                    layout,
                    size=(WINDOW_W,WINDOW_H),
                    icon=APPICON)
window.finalize()
reset_defaults()


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
        v2pdf.FRAME_RATE = values['-SLIDERFRAMERATE-']
        # set fgbg according to framerate
        v2pdf.FGBG_HISTORY = int(values['-SLIDERFRAMERATE-'])*15
        window['-TXTHISTORY-'].update(v2pdf.FGBG_HISTORY)
        # if framerate is updated, syncs the warmup slider as well
        # need to find out how to move the slider actually
        if values['-CKBBINDFRATEWUP-']:
            window['-SLIDERWARMUP-'].update(value=values['-SLIDERFRAMERATE-'])
            v2pdf.WARMUP = values['-SLIDERFRAMERATE-']
    if event == '-SLIDERWARMUP-':
        v2pdf.WARMUP = values['-SLIDERWARMUP-']
    if event == '-SLIDERMINPCT-':
        v2pdf.MIN_PERCENT = values['-SLIDERMINPCT-']
    if event == '-SLIDERMAXPCT-':
        v2pdf.MAX_PERCENT = values['-SLIDERMAXPCT-']
    if event == '-SLIDERTHRESHOLD-':
        v2pdf.VAR_THRESHOLD = values['-SLIDERTHRESHOLD-']
    if event == '-CKBOXSHADOWS-':
        v2pdf.DETECT_SHADOWS = values['-CKBOXSHADOWS-']

    try:
        if event == '-BTNGETOPT-':
            window['-OUT-'].update('')
            sg.Popup(get_current_settings())
    except Exception as e:
        sg.Popup(e)

    # reset options to default values
    if event == '-BTNRESETDEFAULT-':
        reset_defaults()


    # Enable convert button if all data are provided
    if values['-BTNFILE-'] != "" and values['-BTNSAVEFOLDER-'] != "":
        window['-BTNGETPICS-'].update(disabled=False)
    else:
        window['-BTNGETPICS-'].update(disabled=True)

    # merge pics button event
    if event == '-BTNGETPICS-':
        try:
            get_pics()
        except Exception as e:
            print(e)
        
    # merge event    
    if event == '-BTNMERGE-':
        try:
            merge_pics()
        except Exception as e:
            print(e)
        
    

    # window close
    if event == sg.WIN_CLOSED:
        break

window.close()