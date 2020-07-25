import os
from PIL import Image
from pandas import read_pickle

def fix_images(dir_path):
    slash = whichSlash()
    l_images = os.listdir(dir_path)
    for file in l_images:
        img = Image.open(dir_path + slash + file)
        fixed_img = img.resize((200, 200))
        fixed_img.save(dir_path + slash + file, "JPEG", optimize=True)

def whichSlash():
    if os.name == 'posix':
        return('/')
    else:
        return('\\')

def pickle2Dumps(picklePath):
    dumpDict = dict()
    pickleDict = read_pickle(picklePath)
    for trial in pickleDict:
       dumpDict[trial] = pickleDict[trial]['dumps']
    return dumpDict