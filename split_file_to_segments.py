# encoding: utf-8
"""
File:       split_file_to_segments
Author:     twotrees.zf@gmail.com
Date:       2016/08/18 10:40
Desc:       
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from os import path
import subprocess

if __name__ == '__main__':
    message = '''
        Usage:
        python this_file.py [file_to_split] [segments.txt]

        segments.txt format:

        00:03:22
        00:20:99
        00:32:01
        01:33:17

        '''
    print(message)

    sourceFile = sys.argv[1]
    segmentsFile = sys.argv[2]

    segments = None
    with open(segmentsFile, 'r') as f:
        segments = f.read().splitlines()

    segments.insert(0, '00:00:00')

    command = './ffmpeg -v quiet -y -i {0} '.format(sourceFile)
    for i in range(len(segments) - 1):
        baseName, extName = path.splitext(path.basename(sourceFile))
        segmentName = '{0}_{1}{2}'.format(baseName, i + 1, extName)
        segmentPath = path.join(path.dirname(sourceFile), segmentName)
        command += '-vcodec copy -acodec copy -ss {0} -to {1} -sn {2} '.format(segments[i], segments[i + 1], segmentPath)

    subprocess.call(shell=True, args=command)