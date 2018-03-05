# encoding: utf-8
"""
File:       transcode_file
Author:     twotrees.zf@gmail.com
Date:       2016/08/17 16:22
Desc:       
"""

import os
from os import path
import subprocess
import tempfile
import multiprocessing


Commands = {
'VHighProfile_ACopy' : './ffmpeg -i {input} -c:a copy -async 1 ' \
                     '-c:v libx264 -profile:v high422 -preset veryslow ' \
                     '-pix_fmt yuv420p -q:a 0 -sn -threads {cpu_count} -y {output}',

'VHighProfile_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 ' \
                    '-c:v libx264 -profile:v high422 -preset veryslow ' \
                    '-pix_fmt yuv420p -q:a 0 -sn -threads {cpu_count} -y {output}',

'VCopy_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 -c:v copy -y {output}',


'MTS2MP4' : './ffmpeg -i {input} -c:v copy -c:a aac -b:a 256k {output}'
}


def transcodeFile(workspace, sourceFile, command):
    relativePath = path.relpath(sourceFile, workspace)

    tmpFile = path.join(path.dirname(workspace), 'temp', '{}.mp4'.format(hash(os.times())))
    tmpDir = path.dirname(tmpFile)
    if not path.exists(tmpDir):
        os.makedirs(tmpDir)

    cpuCount = min(multiprocessing.cpu_count(), 16)

    exeCommand = command.format(input="'" + sourceFile + "'", output="'" + tmpFile + "'", cpu_count=cpuCount)
    print(exeCommand)
    ret = subprocess.call(shell=True, args=exeCommand)
    if (ret == 0):
        backupFile = path.join(path.dirname(workspace), 'backup', relativePath)
        backupDir = path.dirname(backupFile)
        if not path.exists(backupDir):
            os.makedirs(backupDir)
        os.rename(sourceFile, backupFile)

        doneDir = path.join(path.dirname(workspace), 'done', path.dirname(relativePath))
        if not path.exists(doneDir):
            os.makedirs(doneDir)

        doneFile = path.join(doneDir, path.splitext(path.basename(sourceFile))[0] + '.mp4')
        os.rename(tmpFile, doneFile)
    else:
        if path.exists(tmpFile):
            os.remove(tmpFile)

    return ret
