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

Commands = {
'VHighProfile_ACopy' : './ffmpeg -i {input} -c:a copy -async 1 ' \
                     '-c:v libx264 -profile:v high422 -preset veryslow ' \
                     '-pix_fmt yuv420p -q:a 0 -sn -threads 8 -y {output}',

'VHighProfile_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 ' \
                    '-c:v libx264 -profile:v high422 -preset veryslow ' \
                    '-pix_fmt yuv420p -q:a 0 -sn -threads 8 -y {output}',

'VCopy_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 -c:v copy -y {output}',

# https://wjwoodrow.wordpress.com/2015/07/12/more-ffmpeg-hell/
# Defaults and ranges:
#    Contrast -2.0 to 2.0, default 0 (but I think it is default 1)
#    Brightness -2.0 to 2.0, default 0
#    Saturation 0 to 3, default 1
#    Gamma 0 to 10, default 1
#    Gamma r 0 to 10, default 1
#    Gamma g 0 to 10, default 1
#    Gamma b 0 to 10, default 1
# Order is:
#    contrast : brightness : saturation : gamma : gamma r : gamma g : gamma b : weight
'VHighProfileLighter_AAAC' : './ffmpeg -i {input} ' \
                       '-c:a aac -async 1 ' \
                       '-vf eq=1:0.2:1.5:1:1:1:1:1 ' \
                       '-c:v libx264 -profile:v high422 -preset veryslow ' \
                       '-pix_fmt yuv420p -q:a 0 -sn -threads 8 -y {output}',

'MTS2MP4' : './ffmpeg -i {input} -c:v copy -c:a aac -b:a 256k {output}'
}

def transcodeFile(workspace, sourceFile, command):
    tmpFile = os.path.join(tempfile.gettempdir(), '{}.mp4'.format(hash(os.times())))
    exeCommand = command.format(input=sourceFile, output=tmpFile)
    print(exeCommand)
    ret = subprocess.call(shell=True, args=exeCommand)
    if (ret == 0):
        relativePath = path.relpath(sourceFile, workspace)
        backupFile = path.join(path.dirname(workspace), 'backup', relativePath)
        backupDir = path.dirname(backupFile)
        if not path.exists(backupDir):
            os.makedirs(backupDir)
        os.rename(sourceFile, backupFile)

        destFile = path.join(path.dirname(sourceFile), path.splitext(path.basename(sourceFile))[0] + '.mp4')
        os.rename(tmpFile, destFile)
    else:
        if path.exists(tmpFile):
            os.remove(tmpFile)

    return ret