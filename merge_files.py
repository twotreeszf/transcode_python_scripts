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
    sourceDir = path.join(currentDir, 'workspace')

    sourceFiles = []
    for (dir, dirNames, fileNames) in os.walk(sourceDir):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            if extName.lower() in VIDEO_FORMATS:
                filePath = path.join(sourceDir, fileName)
                sourceFiles.append(filePath)
        break
    sourceFiles = sorted(sourceFiles)

    filesPath = path.join(sourceDir, "files.txt")
    files = open(filesPath, 'w')
    for sourceFile in sourceFiles:
        print('file \'{0}\''.format(sourceFile), file=files)
    files.close()

    baseName, ext = path.splitext(path.basename(sourceFiles[0]))
    destFile = path.join(sourceDir, baseName + '_m' + ext)
    command = './ffmpeg -f concat -safe 0 -i {0} -c copy {1}'.format(filesPath, destFile)
    ret = subprocess.call(shell=True, args=command)
    if ret == 0:
        backupDir = path.join(path.dirname(sourceDir), 'backup')
        if not path.exists(backupDir):
            os.makedirs(backupDir)

        for sourceFile in sourceFiles:
            fileName = path.basename(sourceFile)
            backupFile = path.join(backupDir, fileName)
            os.rename(sourceFile, backupFile)

if __name__ == '__main__':
    batchTanscode()