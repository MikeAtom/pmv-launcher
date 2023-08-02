import PySimpleGUI as sg
import downloader as dw
import datetime
import subprocess
import webbrowser
import sys

sg.theme('DarkGreen6')

# Get current UTC time in unix
currentTime = round(datetime.datetime.now().timestamp())


def convert_to_unix(date):
    return round(datetime.datetime.strptime(date, "%d/%m/%y").timestamp())


def convert_to_days(unix):
    return round(unix / 86400)


def main(gameTests, sampleText, noPreviewPath):


    # List of names of the tests
    testsNames = list(gameTests.keys())
    previewsList = []

    for key in testsNames:
        previewsList.append(gameTests[key]["Icon"])

    previewsList = dw.get_images(previewsList)

    slotsLayout = [[], [], [], [], [], []]
    tileSize = (160, 108)

    for i in range(len(slotsLayout)):
        slotsLayout[i] = [
            [sg.Image(filename=noPreviewPath),
             sg.Text("TBA")],
            [sg.VPush()],
            [sg.Push(), sg.Text("Soon?"), sg.Push()],
            [sg.VPush()]
        ]

    for i in range(len(previewsList)):
        if gameTests[testsNames[i]]["Zip"] == "":
            isDisabled = True
            infoText = "Coming soon"

        elif convert_to_unix(gameTests[testsNames[i]]["ReleaseDate"]) > currentTime:
            isDisabled = True
            releaseDays = convert_to_days(convert_to_unix(gameTests[testsNames[i]]["ReleaseDate"]) - currentTime)
            infoText = f"Releases in {releaseDays} days"

        elif convert_to_unix(gameTests[testsNames[i]]["UpTo"]) < currentTime:
            isDisabled = True
            expiredDays = convert_to_days(currentTime - convert_to_unix(gameTests[testsNames[i]]["UpTo"]))
            infoText = f"Expired {expiredDays} days ago"

        else:
            isDisabled = False
            infoText = f"Left {convert_to_days(convert_to_unix(gameTests[testsNames[i]]['UpTo']) - currentTime)} days"

        if not isDisabled:
            slotsLayout[i] = [
                [sg.Image(filename=previewsList[i]),
                 sg.Text(f"{testsNames[i]}")],
                [sg.Push(), sg.Text(infoText), sg.Push()],
                [sg.Button('Play', enable_events=True, key=f"-{i}-PLAY-", disabled=isDisabled, size=(10, 1)),
                 sg.Button('Form', enable_events=True, key=f"-{i}-FORM-", disabled=isDisabled, size=(5, 1))]
            ]
        else:
            slotsLayout[i] = [
                [sg.Image(filename=previewsList[i]),
                 sg.Text(f"{testsNames[i]}")],
                [sg.VPush()],
                [sg.Push(), sg.Text(infoText), sg.Push()],
                [sg.VPush()]
            ]



    layout = [
        [sg.Text('Build library'), sg.Push(),
         sg.Button('Back', key="-EXIT-")],
        [sg.Frame("", slotsLayout[0], size=tileSize),
         sg.Frame("", slotsLayout[1], size=tileSize),
         sg.Frame("", slotsLayout[2], size=tileSize)],
        [sg.Frame("", slotsLayout[3], size=tileSize),
         sg.Frame("", slotsLayout[4], size=tileSize),
         sg.Frame("", slotsLayout[5], size=tileSize)],
        [sg.Frame("", [[sg.Text(sampleText)]], size=(500, 270))]
    ]

    window = sg.Window('Top Window', layout, size=(530, 360), finalize=True, no_titlebar=True)

    while True:
        event, values = window.read()

        if event.endswith('-PLAY-'):
            # Get the name of the build
            gameName = testsNames[int(event[1])]

            # Download the game build and launch it
            exePath = dw.download_executable(gameTests[gameName]["Zip"])

            # Launch the executable
            subprocess.Popen(exePath)

            window.hide()

            # Check if the game has been closed
            import psutil
            while True:
                if not any("PMV.exe" in s for s in (p.name() for p in psutil.process_iter())):
                    break

            window.un_hide()

        elif event.endswith('-FORM-'):
            # Get the name of the build
            gameName = testsNames[int(event[1])]

            # Open Google Form in browser
            webbrowser.open(gameTests[gameName]["Form"])

        elif event == sg.WIN_CLOSED or event == '-EXIT-':
            break

    window.close()
