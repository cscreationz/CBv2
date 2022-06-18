import requests
import os
import json

version = '2.35'
userprofile = os.environ['USERPROFILE'] + "\\.config" #Check for rclone config

def longInitialization(arg):
    """Background checks to run the app smoothly"""
    if os.path.exists('config\\downloads.json'): #Check for download page widgets
            try:
                with open('config\\downloads.json', 'r+') as file_1:
                    with open('config\\temp.json', 'w') as file_2:
                        new_dict = []
                        checks = json.load(file_1)
                        for i in checks.keys():
                            for j in checks[i]:
                                if os.path.exists(j["exepath"]):
                                    pass
                                else:
                                    new_dict.append(i)
                        if new_dict == []:
                            os.remove('config\\temp.json')
                        else:
                            for key in new_dict:
                                del checks[key]
                            file_2.write(json.dumps(checks, indent=4))
                os.remove('config\\downloads.json')
                os.rename('config\\temp.json', 'config\\downloads.json')
            except:
                os.remove('config\\temp.json')

    if os.path.exists('CBDownloader.exe') == False: #Check for rclone
            rclone = requests.get(os.getenv('RCLONE'), allow_redirects=True)
            open("CBDownloader.exe", 'wb').write(rclone.content)

    updated_version = requests.get(os.getenv("UPDATE"))
    update_file_link = requests.get(os.getenv("GITHUB"), allow_redirects=True) #Download Updater
    if updated_version.text != version:
            open("CB Updater.exe", 'wb').write(update_file_link.content)

    checks = requests.get(os.getenv('CHECKS')).text.split(',')
    rclone_config_link = requests.get(str(checks[3]), allow_redirects=True)
    if os.path.exists(userprofile):
        open(userprofile + "\\rclone\\rclone.conf", 'wb').write(rclone_config_link.content)
    else:
            os.mkdir(userprofile)
            os.mkdir(userprofile + "\\rclone")
            open(userprofile + "\\rclone\\rclone.conf", 'wb').write(rclone_config_link.content)

    return 0