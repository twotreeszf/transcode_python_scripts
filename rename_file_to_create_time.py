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
import platform
from datetime import datetime

def creationDate(path_to_file):
    if platform.system() == 'Windows':
        return path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

def processInFolder(folder):
    for (dir, dirNames, fileNames) in os.walk(folder):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            filePath = path.join(dir, fileName)
            ctime = creationDate(filePath)
            ctime = datetime.fromtimestamp(ctime).strftime('%Y%m%d-%H%M%S')
            newFileName = ctime + extName
            newFilePath = path.join(dir, newFileName)
            if newFileName != filePath:
                os.rename(filePath, newFilePath)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        processInFolder(folder)
