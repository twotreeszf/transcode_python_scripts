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
from transcode_file import Commands

def batchProcess(command):
    currentDir = os.getcwd()
    sourceDir = path.join(currentDir, 'workspace')
    sourceFiles = []

    for (dir, dirNames, fileNames) in os.walk(sourceDir, followlinks=True):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            if extName.lower() in VIDEO_FORMATS:
                filePath = path.join(dir, fileName)
                sourceFiles.append(filePath)

    print('scaned {} source files:'.format(len(sourceFiles)))
    for source in sourceFiles:
        print(source)
    print('\nstart transcoding...')

    successed = []
    failed = []

    for source in sourceFiles:
        print('\nbegin transcode file: {}'.format(source))
        ret = transcodeFile(sourceDir, source, command)
        if ret == 0:
            successed.append(source)
            print('\nsuccess transcode, file: {}'.format(source))
        else:
            failed.append(source)
            print('failed transcode, source file: {}'.format(source))

    print('\nfinishied working')
    print('success files {0}:'.format(len(successed)))
    for file in successed:
        print(file)
    print('\nfailed files {0}'.format(len(failed)))
    for file in failed:
        print(file)

if __name__ == '__main__':
    print('select command to process')

    i = 1
    keys = list(Commands.keys())
    for key in keys:
        print('{0}. {1}'.format(i, key))
        print(Commands[key])
        print('')
        i += 1

    index = None
    try: input = raw_input
    except NameError: pass
    try:
        index = int(input('select:'))
    except ValueError:
        print('Not a number')

    selectedCommand = Commands[keys[index - 1]]
    batchProcess(selectedCommand)