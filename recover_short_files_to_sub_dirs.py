# encoding: utf-8
import sys
import os
from os import path
from rename_to_short_path import processInFolder


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        files = os.listdir(folder)
        for file in files:
            filePath = path.join(folder, file)
            if path.isfile(filePath):
                dir = file.split('_')[0]
                dirPath = path.join(folder, dir)
                if not path.isdir(dirPath):
                    os.mkdir(dirPath)
                newPath = path.join(dirPath, file)
                filePath = path.join(folder, file)
                os.rename(filePath, newPath)