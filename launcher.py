import PySimpleGUI as sg
import downloader as dw
import sys
import pygame

version = 20230731
sg.theme('DarkGreen6')
transparentColor = sg.theme_background_color()

try:
    loadLayout = [
        [sg.Text('Updating Launcher...')],
        [sg.ProgressBar(100, orientation='h', size=(200, 20), bar_color=('#79764C', '#DDEEDF'), key='progressbar')],
        [sg.Text(''), sg.Push(), sg.Button('Cancel', size=(10, 1))]
    ]

    loadWindow = sg.Window('PMV Launcher', loadLayout, size=(400, 100),
                           no_titlebar=True, finalize=True)

    loadWindow.read(timeout=100)

    dwData = dw.get_data()

    icon = dw.get_icon(dwData['icon'])
    images = dw.get_images(dwData['images'])

    loadWindow['progressbar'].UpdateBar(100)
    loadWindow.read(timeout=1000)
    loadWindow.close()





    if dwData['launcherVersion'] > version:
        # Show window with error message
        window = sg.Window('Error', [[sg.Text('Launcher is out of date, please update')]],
                           no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0, 0))
        window.read(timeout=5000)
        sys.exit()

    # if not testing ask for master password
    if not dwData['isTesting']:
        errorLayout = [
            [sg.Text('Enter master password')],
            [sg.Input(key='-IN-')],
            [sg.Button('Submit', key='-SUBMIT-'), sg.Button('Cancel', key='-CANCEL-')]
        ]

        errorWindow = sg.Window('Error', errorLayout, no_titlebar=True, finalize=True, margins=(0, 0),
                                element_padding=(0, 0))

        while True:
            event, values = errorWindow.read()
            if event == '-SUBMIT-':
                if values['-IN-'] == dwData['masterKey']:
                    break
                else:
                    errorWindow['-IN-'].update('')
            elif event == '-CANCEL-' or event == sg.WIN_CLOSED:
                sys.exit()

except Exception as e:
    print(e)
    # Show window with error message
    window = sg.Window('Error', [[sg.Text('Unable to connect to server')]],
                       no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0, 0))
    window.read(timeout=5000)
    sys.exit(0)

backgroundImage = images[0]
windowBackground = sg.Window('Background', [[sg.Image(backgroundImage)]], no_titlebar=True, finalize=True,
                             margins=(0, 0), element_padding=(0, 0), alpha_channel=1)

layout = [
    [sg.Text('')],
    [sg.Push(), sg.Button('Launch', button_color=transparentColor, border_width=0,
                          enable_events=True, key="-START-", font=("Calibli", 18), size=(8, 1))],
    [sg.Push(), sg.Button('Settings', button_color=transparentColor, border_width=0,
                          enable_events=True, key="-OPTIONS-", font=("Calibli", 18), size=(8, 1))],
    [sg.Push(), sg.Button('Support', button_color=transparentColor, border_width=0,
                          enable_events=True, key="-HELP-", font=("Calibli", 18), size=(8, 1))],
    [sg.Push(), sg.Button('Exit', button_color=transparentColor, border_width=0,
                          enable_events=True, key="-EXIT-", font=("Calibli", 18), size=(5, 1))],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text(f"v{dwData['launcherVersion']}")],

]

window = sg.Window('Top Window', layout, size=(690, 388), finalize=True, keep_on_top=True,
                   transparent_color=transparentColor, no_titlebar=True, alpha_channel=1)

while True:
    event, values = window.read()
    if event == '-START-':
        window.hide()
        windowBackground.hide()

        import game
        game.main(dwData['gameTests'], dwData['sampleText'], images[1])

        window.un_hide()
        windowBackground.un_hide()

    elif event == '-OPTIONS-':
        window.hide()
        windowBackground.hide()

        import options
        options.main(icon)

        window.un_hide()
        windowBackground.un_hide()

    elif event == '-HELP-':
        # open browser to support page
        import webbrowser
        webbrowser.open(dwData['supportURL'])
        break

    elif event == '-EXIT-':
        break



window.close()
windowBackground.close()
