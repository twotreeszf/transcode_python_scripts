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
import multiprocessing
import uuid

Commands = {
'VH265High_ACopy' : './ffmpeg -i {input} -c:a copy -async 1 ' \
                     '-c:v libx265 -profile:v main444-8 -preset veryslow ' \
                     '-pix_fmt yuv420p -crf 18 -maxrate 4M -bufsize 4M -sn -threads {cpu_count} -y {output}',

'VH265High_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 ' \
                    '-c:v libx265 -profile:v main444-8 -preset veryslow ' \
                    '-pix_fmt yuv420p -crf 18 -maxrate 4M -bufsize 4M -sn -threads {cpu_count} -y {output}',

'VH264High_ACopy' : './ffmpeg -i {input} -c:a copy -async 1 ' \
                     '-c:v libx264 -profile:v high422 -preset veryslow ' \
                     '-pix_fmt yuv420p -crf 18 -maxrate 4M -bufsize 4M -sn -threads {cpu_count} -y {output}',

'VH264High_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 ' \
                    '-c:v libx264 -profile:v high422 -preset veryslow ' \
                    '-pix_fmt yuv420p -crf 18 -maxrate 4M -bufsize 4M -sn -threads {cpu_count} -y {output}',

'VH264VeryHigh_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 ' \
                    '-c:v libx264 -profile:v high422 -preset veryslow ' \
                    '-pix_fmt yuv420p -crf 18 -maxrate 16M -bufsize 16M -sn -threads {cpu_count} -y {output}',

'VH264HighGray_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 ' \
                    '-c:v libx264 -profile:v high422 -preset veryslow ' \
                    '-vf format=gray -pix_fmt yuv420p -crf 18 -maxrate 4M -bufsize 4M -sn -threads {cpu_count} -y {output}',

'VCopy_AAAC' : './ffmpeg -i {input} -c:a aac -async 1 -c:v copy -y {output}',


'MTS2MP4' : './ffmpeg -i {input} -c:v copy -c:a aac -b:a 256k {output}'
}


def transcodeFile(workspace, sourceFile, command):
    
    relativePath = path.relpath(sourceFile, workspace)

    tmpFile = path.join(path.dirname(workspace), 'temp', '{}.mp4'.format(uuid.uuid4()))
    tmpDir = path.dirname(tmpFile)
    if not path.exists(tmpDir):
        os.makedirs(tmpDir)

    cpuCount = min(multiprocessing.cpu_count(), 16)

    # Split the command into a list and replace placeholders
    cmd_parts = command.split()
    cmd_list = []
    for part in cmd_parts:
        if '{input}' in part:
            cmd_list.append(part.format(input=sourceFile))
        elif '{output}' in part:
            cmd_list.append(part.format(output=tmpFile))
        elif '{cpu_count}' in part:
            cmd_list.append(part.format(cpu_count=cpuCount))
        else:
            cmd_list.append(part)

    print(' '.join(cmd_list))
    ret = subprocess.call(cmd_list)

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
