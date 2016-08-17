# encoding: utf-8
"""
File:       merge_files
Author:     twotrees.zf@gmail.com
Date:       2016/08/17 16:35
Desc:       
"""

from __future__ import print_function
import os
from os import path
import subprocess
from video_formats import VIDEO_FORMATS

def batchTanscode():
    currentDir = os.getcwd()
    sourceDir = path.join(currentDir, 'source')
    destDir = path.join(currentDir, 'dest')

    sourceFiles = []
    for (dir, dirNames, fileNames) in os.walk(sourceDir):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            if extName.lower() in VIDEO_FORMATS:
                filePath = path.join(sourceDir, fileName)
                sourceFiles.append(filePath)
        break
    sourceFiles = sorted(sourceFiles)

    filesPath = path.join(destDir, "files.txt")
    files = open(filesPath, 'w')
    for sourceFile in sourceFiles:
        print('file \'{0}\''.format(sourceFile), file=files)
    files.close()

    destFile = path.join(destDir, path.basename(sourceFiles[0]))
    command = './ffmpeg -f concat -safe 0 -i {0} -c copy {1}'.format(filesPath, destFile)
    subprocess.call(shell=True, args=command)

if __name__ == '__main__':
    batchTanscode()