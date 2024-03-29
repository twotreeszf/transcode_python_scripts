# encoding: utf-8
"""
File:       decrypt_woaiwc
Author:     twotrees.zf@gmail.com
Date:       2018/2/22 21:24
Desc:
"""

import os
import sys
from os import path
from video_formats import VIDEO_FORMATS
from image_formats import IMAGE_FORMATS

def processInFolder(folder):
    for (dir, dirNames, fileNames) in os.walk(folder):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            extName = extName.lower()
            if baseName[0] != '.':
                if extName.lower() in VIDEO_FORMATS or extName.lower() in IMAGE_FORMATS:
                    filePath = path.join(dir, fileName)
                    relativePath = path.relpath(filePath, folder)
                    longFileName = relativePath.replace('/', '_')
                    longFilePath = path.join(folder, longFileName)
                    if longFilePath != filePath:
                        os.rename(filePath, longFilePath)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        processInFolder(folder)
