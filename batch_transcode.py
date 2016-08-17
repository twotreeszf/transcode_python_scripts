# encoding: utf-8
"""
File:       batch_transcode
Author:     twotrees.zf@gmail.com
Date:       2015/06/27 21:52
Desc:       
"""

import os
from os import path
from video_formats import VIDEO_FORMATS
from transcode_file import transcodeFile

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

    print('scaned {} source files:'.format(len(sourceFiles)))
    for source in sourceFiles:
        print(source)
    print('start transcoding...')

    successed = []
    failed = []

    for source in sourceFiles:
        dest = path.join(destDir, path.basename(source))
        print('begin transcode file: {}'.format(source))
        ret = transcodeFile(source, dest)
        if ret == 0:
            successed.append(source)
            print('success transcode, dest file: {}'.format(dest))
        else:
            failed.append(source)
            print('failed transcode, source file: {}'.format(source))

    print('finishied working')
    print('success files:')
    for file in successed:
        print(file)
    print('failed files')
    for file in failed:
        print(file)

if __name__ == '__main__':
    batchTanscode()