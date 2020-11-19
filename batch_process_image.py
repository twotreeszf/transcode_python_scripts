# encoding: utf-8
"""
File:       BatchProcess
Author:     twotrees.zf@gmail.com
Date:       2020年7月2日  27周星期四 15:36
Desc:
"""
import os
from os import path
from image_formats import IMAGE_FORMATS
from compress_image import compressImage
import multiprocessing
from multiprocessing import Pool, Queue


def processTask(sourceDir, source, succQ, failedQ):
    print('\nbegin compress file: {}'.format(source))
    ret = compressImage(sourceDir, source)
    if ret == 0:
        succQ.put(source)
        print('\nsuccess compress, file: {}'.format(source))
    else:
        failedQ.put(source)
        print('failed compress, source file: {}'.format(source))

def batchProcess():
    currentDir = os.getcwd()
    sourceDir = path.join(currentDir, 'workspace')
    sourceFiles = []

    for (dir, dirNames, fileNames) in os.walk(sourceDir, followlinks=True):
        for fileName in fileNames:
            baseName, extName = path.splitext(fileName)
            if extName.lower() in IMAGE_FORMATS:
                filePath = path.join(dir, fileName)
                sourceFiles.append(filePath)

    print('scaned {} source files:'.format(len(sourceFiles)))
    for source in sourceFiles:
        print(source)
    print('\nstart compress...')

    successed = multiprocessing.Manager().Queue()
    failed = multiprocessing.Manager().Queue()
    cpuCount = multiprocessing.cpu_count()

    with Pool(processes=cpuCount) as pool:
        results = []
        for source in sourceFiles:
            result = pool.apply_async(processTask, (sourceDir, source, successed, failed))
            results.append(result)

        for result in results:
            result.get()

        pool.close()
        pool.join()

    print('\nfinishied working')
    successedFiles = []
    while not successed.empty():
        successedFiles.append(successed.get())
    print('success files {0}:'.format(len(successedFiles)))
    for file in successedFiles:
        print(file)

    failedFiles = []
    while not failed.empty():
        failedFiles.append(failed.get())
    print('\nfailed files {0}'.format(len(failedFiles)))
    for file in failedFiles:
        print(file)

if __name__ == '__main__':
    batchProcess()