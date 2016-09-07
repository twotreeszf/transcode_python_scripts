# encoding: utf-8
"""
File:       transcode_file
Author:     twotrees.zf@gmail.com
Date:       2016/08/17 16:22
Desc:       
"""

import subprocess

class Commands(object):
    Hi422LosslesAudioCopy = './ffmpeg -i {input} -c:a copy -async 1 ' \
                            '-c:v libx264 -profile:v high422 -preset veryslow ' \
                            '-pix_fmt yuv420p -q:a 0 -sn -threads 8 -y {output}'

    Hi422LosslesAudioAAC = './ffmpeg -i {input} -c:a aac -async 1 ' \
                            '-c:v libx264 -profile:v high422 -preset veryslow ' \
                            '-pix_fmt yuv420p -q:a 0 -sn -threads 8 -y {output}'

    VideoCopyAudioAAC    = './ffmpeg -i {input} -c:a aac -async 1 -c:v copy -y {output}'

    '''
    https://wjwoodrow.wordpress.com/2015/07/12/more-ffmpeg-hell/

    Defaults and ranges:
        Contrast -2.0 to 2.0, default 0 (but I think it is default 1)
        Brightness -2.0 to 2.0, default 0
        Saturation 0 to 3, default 1
        Gamma 0 to 10, default 1
        Gamma r 0 to 10, default 1
        Gamma g 0 to 10, default 1
        Gamma b 0 to 10, default 1

    Order is:
        contrast : brightness : saturation : gamma : gamma r : gamma g : gamma b : weight
    '''
    Hi422VideoLighterAudioAAC = './ffmpeg -i {input} '\
                                '-c:a aac -async 1 '\
                                '-vf eq=1:0.2:1.5:1:1:1:1:1 '\
                                '-c:v libx264 -profile:v high422 -preset veryslow '\
                                '-pix_fmt yuv420p -q:a 0 -sn -threads 8 -y {output}'

def transcodeFile(sourceFile, destFile):
    command = Commands.Hi422LosslesAudioCopy.format(input=sourceFile, output=destFile)
    print(command)
    return subprocess.call(shell=True, args=command)