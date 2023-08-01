import downloader as dw
import subprocess
import os
import sys

pmvFolder = os.path.join(os.getenv('LOCALAPPDATA'), 'PMV/Launcher')

# Launcher.20230800.exe
version = 0

if not os.path.exists(pmvFolder):
    os.makedirs(pmvFolder)
    files = []
else:
    #List all the files in the directory that end in .exe
    files = [f for f in os.listdir(pmvFolder) if f.endswith('.exe')]

    #If there are no files in the directory, update
    if len(files) == 1:
        # Check launcher version from file name
        version = int(files[0].split('.')[1])

dwData = dw.get_data()

if dwData['launcherVersion'] > version:
    # Delete all the files in the directory
    for file in files:
        os.remove(os.path.join(pmvFolder, file))

    # Update launcher
    dw.update_launcher(dwData['launcherURL'], os.path.join(pmvFolder, f'Launcher.{dwData["launcherVersion"]}.exe'))


# Launch launcher
subprocess.Popen(os.path.join(pmvFolder, f'Launcher.{dwData["launcherVersion"]}.exe'))
sys.exit()
