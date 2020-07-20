# encoding: utf-8
"""
File:       decode_hidden_files
Author:     twotrees.zf@gmail.com
Date:       2020年7月19日  30周星期日 17:12
Desc:
"""

import sys
import mmap
import os
from os import path
from video_formats import VIDEO_FORMATS


def decodeFile(filePath):
    with open(filePath, 'r+b') as file:
        mm = mmap.mmap(file.fileno(), 0)
        index = mm.rfind(b'hide')
        if index == -1:
            print('no magic data was found:{0}'.format(filePath))
            return
        file.seek(index)
        file.write(b'moov')

def decodeInFolder(folder):
    for (dir, dirNames, fileNames) in os.walk(folder):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            if extName.lower() in VIDEO_FORMATS:
                filePath = path.join(dir, fileName)
                decodeFile(filePath)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        decodeInFolder(folder)
