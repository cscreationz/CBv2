import os, json, pickle
from PySide2.QtWidgets import QFileDialog
from PySide2.QtCore import QProcess
#import psutil
import requests
import zipfile

def browseFile():
    fileDirectory = QFileDialog.getExistingDirectory()
    return fileDirectory

def readjson(file):
    with open(file, 'r+') as f:
        data = json.load(f)
    return f, data

def writejson(file):
    with open(file, 'w') as f:
        return f

def readbinary(file: str) -> str:
    """Returns binary data from a given file as a string"""
    with open(file, 'rb') as f:
        data: str = pickle.load(f)
    return data

'''def freeDiskSpace(text):
    freeSpace = cb_utils.convert_size(psutil.disk_usage(text[0:2]).free)
    return freeSpace'''

def verifyLocation(directory):
    if directory.endswith("\\"):
        return False

'''def createShortcut(directory, download_location, game_name, exepath):
    path = os.path.join(directory, f"{game_name}.lnk")
    target = f"{download_location}\\{game_name}{exepath}"
    wDir = f"{download_location}\\{game_name}"
    icon = f"{download_location}\\{game_name}{exepath}"
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()'''

def countMatchedSaves(stdout, game_name):
    matched_save_counter = 0
    try:
        replaced_text = stdout.replace('/', '')
        split_text = replaced_text.split('\n')
        for i in split_text:
            if game_name == i:
                matched_save_counter += 1
        return matched_save_counter
    except:
        pass

def rewriteJsonFile(fileObject, jsonObject):
    fileObject.seek(0)
    fileObject.write(json.dumps(jsonObject, indent=4))
    fileObject.truncate()

def writeJsonFile(fileObject, jsonObject):
    fileObject.write(json.dumps(jsonObject, indent=4))

def updateExistingJson(x, game_name, image, download_location, exepath):
    x[game_name.replace(' ', '_').lower() + "_download"] = [
        {
            "game_name":f"{game_name}",
            "image":f"{image}",
            "exepath":f"{download_location + '/' + game_name + exepath}",
            "download_location":f"{download_location + '/' + game_name}"
        }
    ]
    return x

def createNewJson(game_name, image, download_location, exepath):
    x = {game_name.replace(' ', '_').lower() + "_download":[
            {
                "game_name":f"{game_name}",
                "image":f"{image}",
                "exepath":f"{download_location + '/' + game_name + exepath}",
                "download_location":f"{download_location + '/' + game_name}"
            }
        ]
    }
    return x

def downloadMissingFiles(download_location, game_name, link, file_name):
    if os.path.exists(download_location + f"\\{game_name}") == False:
        os.mkdir(download_location + f"\\{game_name}")
    r = requests.get(link, allow_redirects=True)    
    open(download_location + f"\\{game_name}" + f"\\{file_name}", 'wb').write(r.content)

def downloadMissingZip(download_location, game_name, link, file_name):
    if os.path.exists(download_location + f"\\{game_name}") == False:
        os.mkdir(download_location + f"\\{game_name}")
    r = requests.get(link, allow_redirects=True)
    open(download_location + f"\\{game_name}" + f"\\{file_name}", "wb").write(r.content)
    with zipfile.ZipFile(download_location + f"\\{game_name}" + f"\\{file_name}", 'r') as zip_ref:
        zip_ref.extractall(download_location + f"\\{game_name}")
    os.remove(download_location + f"\\{game_name}" + f"\\{file_name}")

def checkIfMissingFiles(fix_games, game_name):
    missingFileCounter = 0
    for i in fix_games:
        if game_name == i:
            missingFileCounter += 1
    return missingFileCounter

def retrieveMissingFileDetail(fix_games, game_name):
    for i in fix_games[game_name]:
        link = i["link"]
        file_name = i["file_name"]
        type_of_file = i["type"]
    return link, file_name, type_of_file
