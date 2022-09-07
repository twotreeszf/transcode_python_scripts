# encoding: utf-8
"""
File:       decrypt_woaiwc
Author:     twotrees.zf@gmail.com
Date:       2018/2/22 21:24
Desc:
"""

import os
import sys
import shutil
from os import path
from video_formats import VIDEO_FORMATS
from image_formats import IMAGE_FORMATS

def processInFolder(folder):
    dirMap = {}
    for (dir, dirNames, fileNames) in os.walk(folder):
        if dir in dirMap:
            shortRoot = dirMap[dir]
        else:
            shortRoot = dir

        dirNames.sort()
        for dirName in dirNames:
            index = dirNames.index(dirName) + 1
            shortDir = '{0}'.format(index)
            shortDir = path.join(shortRoot, shortDir)
            fullDir = path.join(dir, dirName)

            dirMap[fullDir] = shortDir

        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            extName = extName.lower()
            if baseName[0] != '.':
                if extName.lower() in VIDEO_FORMATS or extName.lower() in IMAGE_FORMATS:
                    filePath = path.join(dir, fileName)
                    if dir in dirMap:
                        shortDir = dirMap[dir]
                        relDir = path.relpath(shortDir, folder)
                        relDir = relDir.replace('/', '_')
                        shortName = '{0}_{1}'.format(relDir, fileName)
                        shortPath = path.join(folder, shortName)
                        os.rename(filePath, shortPath)

    files = os.listdir(folder)
    for file in files:
        filePath = path.join(folder, file)
        if path.isdir(filePath):
            shutil.rmtree(filePath)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        processInFolder(folder)
