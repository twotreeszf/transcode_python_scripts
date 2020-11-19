# encoding: utf-8
"""
File:       CompressImage
Author:     twotrees.zf@gmail.com
Date:       2020年7月2日  27周星期四 15:43
Desc:
"""
from PIL import Image
import os
import shutil
from os import path
import uuid


def compressImage(workspace, sourceFile):
    relativePath = path.relpath(sourceFile, workspace)

    tmpFile = path.join(path.dirname(workspace), 'temp', '{}.jpg'.format(uuid.uuid4()))
    tmpDir = path.dirname(tmpFile)
    if not path.exists(tmpDir):
        os.makedirs(tmpDir)

    ret = resizeImage(sourceFile, tmpFile)
    if (ret == 0):
        backupFile = path.join(path.dirname(workspace), 'backup', relativePath)
        backupDir = path.dirname(backupFile)
        if not path.exists(backupDir):
            os.makedirs(backupDir)
        shutil.move(sourceFile, backupFile)

        doneDir = path.join(path.dirname(workspace), 'done', path.dirname(relativePath))
        if not path.exists(doneDir):
            os.makedirs(doneDir)

        doneFile = path.join(doneDir, path.splitext(path.basename(sourceFile))[0] + '.jpg')
        shutil.move(tmpFile, doneFile)
    else:
        if path.exists(tmpFile):
            os.remove(tmpFile)

    return ret

def resizeImage(source_path, dest_path):
    # resize image
    try:
        image = Image.open(source_path)

        newSize = (int(image.size[0] * 0.8), int(image.size[1] * 0.8))
        newImage = image.resize(newSize, Image.LANCZOS)

        exif = image.info['exif']
        newImage.save(dest_path, "JPEG", exif=exif, quality=90)

        image.close()
        newImage.close()
    except:
        return 1

    return 0