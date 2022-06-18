import os
import pickle
import math
from typing import List
import win32com
import json

def check_if_files_exist(folders: List[str]) -> None: 
    """Creates a folder if it doesn't exist"""
    for folder in folders:
        if os.path.exists(folder) == False:
            os.mkdir(folder)

def delete_files(files: List[str]) -> None:
    """Deletes given folder"""
    try:
        for file in files:
            os.remove(file)
    except:
        pass

def readbinary(file: str) -> str:
    """Returns binary data from a given file as a string"""
    with open(file, 'rb') as f:
        data: str = pickle.load(f)
    return data

def readjson(file):
    with open(file, 'r+') as f:
        data = json.load(f)
    return f, data

def writejson(file):
    with open(file, 'w') as f:
        return f

def writebinary(file: str, details: List[str, bytes]) -> None:
    """Writes a binary file to a given location with the given details"""
    with open(file, 'wb') as f:
        pickle.dump(details, f)

def convert_size(size_bytes):
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def createshortcut(destination, download_location, pc_user, game_name, exepath):
    path = os.path.join(destination, f"{game_name}.lnk")
    target = f"{download_location}\\{game_name}{exepath}"
    wDir = f"{download_location}\\{game_name}"
    icon = f"{download_location}\\{game_name}{exepath}"
    shell = win32com.client.Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()