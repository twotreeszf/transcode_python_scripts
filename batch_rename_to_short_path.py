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
            if path.isdir(filePath):
                processInFolder(filePath)