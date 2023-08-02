import os
import urllib.request
import json
import master_url
import zipfile

tempDir = os.path.join(os.getenv('LOCALAPPDATA'), 'temp/pmv')

if os.path.exists(tempDir):
    # Delete all the files in the directory
    for file in os.listdir(tempDir):
        os.remove(os.path.join(tempDir, file))

    # Delete the directory
    os.rmdir(tempDir)

os.makedirs(tempDir)


def get_data():
    path = os.path.join(tempDir, 'pmvinfo.tmp')

    # Download the file from `url` and save it locally under `path`:
    with urllib.request.urlopen(master_url.URL) as response, open(path, 'wb') as out_file:
        data = response.read()  # a `bytes` object
        out_file.write(data)

    # Open the file as json and read the contents
    with open(path, 'r') as json_file:
        contents = json.load(json_file)

    # Delete the file
    os.remove(path)

    return contents


def get_icon(url):
    # Download the file from `url` and reade base64 string
    with urllib.request.urlopen(url) as response:
        data = response.read()

    return data


def get_images(urlList):
    filesPathsList = []
    i = len(os.listdir(tempDir))

    for url in urlList:
        path = os.path.join(tempDir, f'{i}con.tmp')

        # Download the file from `url` and save it locally under `path`:
        with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        i += 1
        filesPathsList.append(path)

    return filesPathsList


def update_launcher(url, path):
    # Download the file from `url` and save it locally under `path`:
    with urllib.request.urlopen(url) as response, open(os.path.join(path), 'wb') as out_file:
        data = response.read()
        out_file.write(data)


def download_executable(zipURL):
    pathZip = os.path.join(tempDir, 'tmp.zip')
    pathExe = os.path.join(tempDir, 'PMV.exe')
    pathUnpack = os.path.join(tempDir)

    # Download the file from `url` and save it locally under `path`:
    with urllib.request.urlopen(zipURL) as response, open(pathZip, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

    # Unpack the zip file
    with zipfile.ZipFile(pathZip, 'r') as zip_ref:
        zip_ref.extractall(pathUnpack)

    return pathExe
