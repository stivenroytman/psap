import os
from PIL import Image
from pandas import read_pickle

def fix_images(dir_path):
    l_images = os.listdir(dir_path)
    for file in l_images:
        img = Image.open(os.path.join(dir_path, file))
        fixed_img = img.resize((200, 200))
        if file.split('.')[1] == 'png':
            fixed_img.save(os.path.join(dir_path, file), "PNG", optimize=True)
        else:
            fixed_img.save(os.path.join(dir_path, file), "JPEG", optimize=True)

def pickle2Dumps(picklePath):
    dumpDict = dict()
    pickleDict = read_pickle(picklePath)
    for trial in pickleDict:
       dumpDict[trial] = pickleDict[trial]['dumps']
    return dumpDict
