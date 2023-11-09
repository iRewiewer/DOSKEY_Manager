from json import loads, dumps
from os import walk, getenv, path
from shutil import copyfile
from random import randint
from argparse import ArgumentParser

# Global configuration dictionary
CONFIG = {}


# Retrieve the path of the DOSKEY Manager application
def GetAppFolderPath():
    from winreg import OpenKey, HKEY_LOCAL_MACHINE, QueryValueEx, CloseKey
    keyPath = r"SOFTWARE\Microsoft\Command Processor"
    try:
        hkey = OpenKey(HKEY_LOCAL_MACHINE, keyPath)
        pathValue, _ = QueryValueEx(hkey, "DoskeyManagerPath")
        CloseKey(hkey)
        return pathValue[1:-len('DOSKEY_Loader.bat')-1]
    except Exception as e:
        print(f"An error occurred getting app path from registry. Create issue on GitHub and copy paste this message there.\nError: {e}")


# Load configuration from a JSON file
def LoadConfig():
    global CONFIG
    configPath = rf"{GetAppFolderPath()}config.json"
    if(path.exists(configPath)):
        CONFIG = loads(open(configPath, 'r').read())
    else:
        CONFIG = {
            "winStoreLocation": "%appdata%\\Local\\Packages"
        }

        try:
            open(configPath, "w").write(dumps(CONFIG, indent=4))
        except Exception as e:
            print(f"Error creating config. Create issue on GitHub and copy paste this message there.\nError: {e}")


# Construct the path to the Windows Terminal directory
def WinTerminalDirectory():
    if ("%appdata%" in CONFIG["winStoreLocation"]):
        return CONFIG["winStoreLocation"].replace("%appdata%", getenv('APPDATA')[:-len("Roaming")-1])
    else:
        return CONFIG["winStoreLocation"]


# Change the Windows Terminal background
def ChangeBackground(backgroundsPath, jsonPath, json, type):
    images = {}
    atRoot = True

    try:
        # Walk through the backgrounds folder and get the images
        for item in walk(backgroundsPath):
            if atRoot == True:
                atRoot = False
                rootPath = item[0]
                folders = item[1]
                if type not in folders and type != "random":
                    type = "random"
                    print(f"Couldn't find a background folder called '{type}'. Changing to a random one.")

                images["root"] = []
                images["random"] = []
                for i in item[2]:
                    images["root"].append(f"{rootPath}\\{i}")
                    images["random"].append(f"{rootPath}\\{i}")
            else:
                rootPath = item[0]
                folderName = rootPath.split("\\")[-1]
                images[folderName] = []
                for i in item[2]:
                    images[folderName].append(f"{rootPath}\\{i}")
                    images["random"].append(f"{rootPath}\\{i}")
    except Exception as e:
        print(f"Error loading images from backgrounds folder. Create issue on GitHub and copy paste this message there.\nError: {e}")
        return False

    try:
        if ("backgroundImage" in json["profiles"]["defaults"]):
            currentBackground = json["profiles"]["defaults"]["backgroundImage"]
        else:
            currentBackground = None
        newBackground = images[type][randint(0, len(images[type]) - 1)]
        while currentBackground == newBackground:
            newBackground = images[type][randint(0, len(images[type]) - 1)]

        # Update the background image and opacity in the JSON
        json["profiles"]["defaults"]["backgroundImage"] = newBackground
        json["profiles"]["defaults"]["backgroundImageOpacity"] = 0.26

        # Write the updated JSON back to the settings file
        file = dumps(json, indent=4)
        open(jsonPath, 'w').write(file)
    except:
        print(
            f"Error applying a new background.")
        return False
    return True


# Main application function
def App():
    LoadConfig()

    jsonPath = rf"{WinTerminalDirectory()}\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
    backgroundsPath = rf"{GetAppFolderPath()}backgrounds"

    try:
        json = loads(open(jsonPath, 'r').read())
        # Make backup in case of failure
        copyfile(jsonPath, rf"{GetAppFolderPath()}settingsBackup.json")
    except Exception as e:
        print(f"Error reading JSON via background changer script. Create issue on GitHub and copy paste this message there.\nError: {e}")
        return False

    # Parse command-line arguments
    parser = ArgumentParser(prog="bg")
    parser.add_argument('-type')
    args = parser.parse_args()

    if args.type == None:
        args.type = "random"

    # Load backup in case of failure
    if not ChangeBackground(backgroundsPath, jsonPath, json, args.type):
        copyfile(rf"{GetAppFolderPath()}settingsBackup.json", jsonPath)


if "__main__" == __name__:
    App()
