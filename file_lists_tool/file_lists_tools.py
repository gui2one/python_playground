# import glob
# var = glob.glob('E:/TEMP/backup/*[0-9]*.*')
# print var

import fnmatch
import os

for file in os.listdir('E:/TEMP/AMP_TDV_2013/3D_render/openGL'):
    if fnmatch.fnmatch(file, '*[0-9].*'):
        print file