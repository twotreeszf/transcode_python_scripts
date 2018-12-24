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

def processInFolder(folder):
    for (dir, dirNames, fileNames) in os.walk(folder):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            filePath = path.join(dir, fileName)

            if len(baseName) > 64:
                baseName = baseName[:64]
                fileName = baseName + extName;
                newPath = path.join(dir, fileName)

                print('rename {0} \n to \n {1}'.format(filePath, newPath))
                os.rename(filePath, newPath)

            newName = baseName.replace('%', '_')
            if (newName != baseName):
                fileName = newName + extName;
                newPath = path.join(dir, fileName)

                print('rename {0} \n to \n {1}'.format(filePath, newPath))
                os.rename(filePath, newPath)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        processInFolder(folder)
