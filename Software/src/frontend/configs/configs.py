import json
import os

APP_DIR = "cacho"
DIR_IMAGE = "Picture"
DIR_VIDEO = "Video"
DIR_DATA = "Data"

LOGO_2 = "logo_2.png"

APP_NAME = ""
INFORMATION = {}


######################Last#########################
# with open("./configs/configs.json", "r") as file:~
    # INFORMATION = json.load(file)
    # APP_NAME = INFORMATION["name"]
# def load_language(lang="en_En"):
#     data = []
#     if lang == "en_En":
#         with open("./lang/en_En.json", "r") as file:
#             data = json.load(file)
#     else:
#         with open("./lang/%s.json"%lang, "r") as file:
#             data = json.load(file)
#     return data
########################Last##########################


#############New#####################################################
def loadJsonFile(file):
    with open(os.path.join(os.path.dirname(__file__),file), "r") as file:
        data = json.load(file)
    return data

INFORMATION=loadJsonFile("configs.json")
APP_NAME = INFORMATION["name"]

def load_language(lang="en_En"):
    data = []
    if lang == "en_En":
        data=loadJsonFile("./../lang/en_En.json")
    else:
        data=loadJsonFile("./../lang/%s.json"%lang)
    return data



