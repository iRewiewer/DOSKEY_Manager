from json import loads, dumps
from os import listdir, environ
from shutil import copyfile
from random import randint
from argparse import ArgumentParser

colors = [
    "random",
    "blue",
    "gold",
    "green",
    "purple",
    "red"
]

def ChangeBackground(backgroundsPath, jsonPath, color = "random"):
    images = []
    
    for image in listdir(backgroundsPath):
        images.append(f"{backgroundsPath}\\{image}")

    json["profiles"]["defaults"]["backgroundImage"] = images[randint(0, len(images) - 1)]
    json["profiles"]["defaults"]["backgroundImageOpacity"] = 0.26

    file = dumps(json, indent = 4)
    open(jsonPath, 'w').write(file)

if "__main__" == __name__:
    # parser = ArgumentParser(prog = "bg")
    # parser.add_argument('-color', choices = colors)
    # args = parser.parse_args()

    try:
        jsonPath = r"C:\Users\iRewiewer\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
        backgroundsPath = rf"{environ['doskeyLocalPath']}\backgrounds"

        json = loads(open(jsonPath, 'r').read())
        copyfile(jsonPath, rf"{backgroundsPath}\..\settingsBackup.json") # create backup
    except:
        print("Error reading JSON via background changer script.")

    try:
        ChangeBackground(backgroundsPath, jsonPath)
    except:
        print(f"Error changing background. Reloading JSON from backup.\nJSON Path: {jsonPath}")
        copyfile(rf"{backgroundsPath}\..\settingsBackup.json", jsonPath)