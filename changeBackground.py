from json import loads, dumps
from os import environ, walk
from shutil import copyfile
from random import randint
from argparse import ArgumentParser

file = open

def ChangeBackground(backgroundsPath, jsonPath, type):
    images = {}
    atRoot = True

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

    currentBackground = json["profiles"]["defaults"]["backgroundImage"]
    newBackground = images[type][randint(0, len(images[type]) - 1)]
    while currentBackground == newBackground:
        newBackground = images[type][randint(0, len(images[type]) - 1)]

    json["profiles"]["defaults"]["backgroundImage"] = newBackground
    json["profiles"]["defaults"]["backgroundImageOpacity"] = 0.26

    file = dumps(json, indent = 4)
    open(jsonPath, 'w').write(file)

if "__main__" == __name__:
    try:
        jsonPath = r"C:\Users\iRewiewer\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
        backgroundsPath = rf"{environ['doskeyLocalPath']}backgrounds"

        json = loads(open(jsonPath, 'r').read())
        copyfile(jsonPath, rf"{backgroundsPath}\..\settingsBackup.json") # create backup
    except:
        print("Error reading JSON via background changer script.")

    parser = ArgumentParser(prog = "bg")
    parser.add_argument('-type')
    args = parser.parse_args()

    try:
        if args.type == None:
            args.type = "random"

        ChangeBackground(backgroundsPath, jsonPath, args.type)
    except:
        print(f"Error changing background. Reloading JSON from backup.\nJSON Path: {jsonPath}")
        copyfile(rf"{backgroundsPath}\..\settingsBackup.json", jsonPath)