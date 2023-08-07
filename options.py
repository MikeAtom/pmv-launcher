import PySimpleGUI as sg
import pygame
import os


settingsDir = os.path.join(os.getenv('LOCALAPPDATA'), 'PMV')
settingsFile = "settings.ini"
settingsFilePath = os.path.join(settingsDir, settingsFile)

if not os.path.exists(settingsDir):
    os.makedirs(settingsDir)


def write_settings():
    global userResolution, userDisplayMode, userGraphicsQuality, userVSync, userController, userPrompt, userLanguage

    with open(settingsFilePath, 'w') as settingsFile:
        settingsFile.write(
            '[Video]\n'
            f'resolution="{userResolution}"\n'
            f'displayMode="{userDisplayMode}"\n'
            f'graphicsQuality="{userGraphicsQuality}"\n'
            f'vsync="{userVSync}"\n'
            '\n'
            '[Controls]\n'
            f'confirmType="{userController}"\n'
            f'prompts="{userPrompt}"\n'
            '\n'
            '[Other]\n'
            f'language="{userLanguage}"'
        )


def write_default_setting():
    global userResolution, userDisplayMode, userGraphicsQuality, userVSync, userController, userPrompt, userLanguage, inputDevicesList

    inputDevicesList = ['Keyboard + Mouse'] + [i.split(" - ")[1] for i in
                                               [f"{i} - {pygame.joystick.Joystick(i).get_name()}" for i in
                                                range(pygame.joystick.get_count())]]

    userController = inputDevicesList[-1]

    get_prompt()

    userResolution = "1600x900"
    userDisplayMode = "Borderless"
    userGraphicsQuality = "High"
    userVSync = "On"
    userLanguage = "English"


def get_prompt():
    global userController, userPrompt

    if userController != "Keyboard + Mouse":
        if "PS4" in userController or "PS5" in userController:
            userPrompt = "Playstation"
        elif "Xbox" in userController:
            userPrompt = "Xbox"
        elif "Nintendo" in userController:
            userPrompt = "Nintendo"
    else:
        userPrompt = "Keyboard"

def check_if_settings_file_exists():
    if not os.path.exists(settingsFilePath):
        write_default_setting()
        return False
    else:
        return True

def main(icon):
    sg.theme('Default1')

    global userResolution, userDisplayMode, userGraphicsQuality, userVSync, userController, userPrompt, userLanguage, inputDevicesList

    pygame.joystick.init()
    inputDevicesList = ['Keyboard + Mouse'] + [i.split(" - ")[1] for i in
                                               [f"{i} - {pygame.joystick.Joystick(i).get_name()}" for i in
                                                range(pygame.joystick.get_count())]]
    promptsList = ['Nintendo', 'Playstation', 'Playstation, Japan Confirm', 'Xbox', 'Keyboard']
    resolutionList = ['1920x1080', '1600x900', '1280x720', '640x360']
    displayModeList = ['Fullscreen', 'Windowed', 'Borderless']
    graphicsQualityList = ['Low', 'Medium', 'High']
    languageList = ['English', 'Ukrainian']

    userResolution = ""
    userDisplayMode = ""
    userGraphicsQuality = ""
    userVSync = ""
    userController = ""
    userPrompt = ""
    userLanguage = ""

    # check if exists settings file
    # if not then create one with default settings
    # if exists then read settings from it
    if check_if_settings_file_exists():
        with open(settingsFilePath, 'r') as settingsFile:
            settings = settingsFile.readlines()

        userResolution = settings[1].split('"')[1]
        userDisplayMode = settings[2].split('"')[1]
        userGraphicsQuality = settings[3].split('"')[1]
        userVSync = settings[4].split('"')[1]
        userController = settings[7].split('"')[1]
        userPrompt = settings[8].split('"')[1]
        userLanguage = settings[11].split('"')[1]

        if userController not in inputDevicesList:
            userController = inputDevicesList[-1]

    write_settings()

    videoLayout = [
        [sg.Push(),
         sg.Text('Resolution', size=(12, 1), justification="Right"),
         sg.Combo(resolutionList, default_value=userResolution, size=(35, 1), enable_events=True, key="-RESOLUTION-"),
         sg.Push()],
        [sg.Push(),
         sg.Text('Display Mode', size=(12, 1), justification="Right"),
         sg.Combo(displayModeList, default_value=userDisplayMode, size=(35, 1), enable_events=True,
                  key="-DISPLAY-MODE-"),
         sg.Push()],
        [sg.Push(),
         sg.Text('Graphics Quality', size=(12, 1), justification="Right"),
         sg.Combo(graphicsQualityList, default_value=userGraphicsQuality, size=(35, 1), enable_events=True,
                  key="-GRAPHICS-QUALITY-"),
         sg.Push()],
        [sg.Push(),
         sg.Text('VSync', size=(12, 1), justification="Right"),
         sg.Combo(['On', 'Off'], default_value=userVSync, size=(35, 1), enable_events=True, key="-VSYNC-"),
         sg.Push()],

    ]
    controlsLayout = [
        [sg.Push(),
         sg.Text('Input Device', size=(12, 1), justification="Right"),
         sg.Combo(inputDevicesList, default_value=userController, size=(35, 1), enable_events=True,
                  key="-INPUT-DEVICE-"),
         sg.Push()],
        [sg.Push(),
         sg.Text('Prompts', size=(12, 1), justification="Right"),
         sg.Combo(promptsList, default_value=userPrompt, size=(35, 1), enable_events=True, key="-PROMPTS-"),
         sg.Push()]
    ]

    otherLayout = [
        [sg.Push(),
         sg.Text('Language', size=(12, 1), justification="Right"),
         sg.Combo(languageList, default_value=userLanguage, size=(35, 1), enable_events=True, key="-LANGUAGE-"),
         sg.Push()]
    ]

    buttonsLayout = [
        [sg.Button('Default', size=(10, 1), enable_events=True, key="-DEFAULT-"),
         sg.Push(),
         sg.Button('Apply', size=(10, 1), enable_events=True, key="-APPLY-"),
         sg.Button('Back', size=(10, 1), enable_events=True, key="-BACK-")]

    ]

    layout = [
        [sg.Frame('Video', videoLayout, size=(456, 128))],
        [sg.Frame('Controls', controlsLayout, size=(456, 74))],
        [sg.Frame('Other', otherLayout, size=(456, 48))],
        [buttonsLayout]
    ]
    # no icon
    window = sg.Window('PMV Options', layout, size=(456, 320), finalize=True, icon=icon, keep_on_top=True)

    while True:
        event, values = window.read()
        if event == '-RESOLUTION-':
            userResolution = values['-RESOLUTION-']
        elif event == '-DISPLAY-MODE-':
            userDisplayMode = values['-DISPLAY-MODE-']
        elif event == '-GRAPHICS-QUALITY-':
            userGraphicsQuality = values['-GRAPHICS-QUALITY-']
        elif event == '-VSYNC-':
            userVSync = values['-VSYNC-']
        elif event == '-INPUT-DEVICE-':
            userController = values['-INPUT-DEVICE-']
            get_prompt()
            window['-PROMPTS-'].update(value=userPrompt)
        elif event == '-PROMPTS-':
            userPrompt = values['-PROMPTS-']
        elif event == '-LANGUAGE-':
            userLanguage = values['-LANGUAGE-']
        elif event == '-DEFAULT-':
            write_default_setting()
            window['-RESOLUTION-'].update(value=userResolution)
            window['-DISPLAY-MODE-'].update(value=userDisplayMode)
            window['-GRAPHICS-QUALITY-'].update(value=userGraphicsQuality)
            window['-VSYNC-'].update(value=userVSync)
            window['-INPUT-DEVICE-'].update(value=userController)
            window['-PROMPTS-'].update(value=userPrompt)
            window['-LANGUAGE-'].update(value=userLanguage)
        elif event == '-APPLY-':
            write_settings()
        elif event == '-BACK-' or event == sg.WIN_CLOSED:
            break

    window.close()
