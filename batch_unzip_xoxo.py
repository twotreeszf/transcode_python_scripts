# encoding: utf-8
import sys
import os
from os import path
import subprocess

def batch_unzip_folders(root_folder):
    folders = [f for f in os.listdir(root_folder) if path.isdir(path.join(root_folder, f))]
    for folder in folders:
        split = folder.split('^')
        if len(split) != 2:
            continue
        password = split[1]

        try:
            unzip_folder(path.join(root_folder, folder), password)
        except Exception as e:
            print(e)

def unzip_folder(folder, password):
    zip_files =[]
    for root, dirs, files in os.walk(folder):
        for file in files:
            if path.splitext(file)[1] == '.zip':
                zip_files.append(path.join(root, file))

    for zip in zip_files:
        folder = path.dirname(zip)
        print('extracting:{0}'.format(zip))
        subprocess.call(['keka', '7z', 'x', zip, '-o{0}'.format(folder), '-p{0}'.format(password)])
        os.remove(zip)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        message = '''
                Usage:
                python batch_unzip_xoxo.py [root_folder]
                '''
        print(message)
        exit(1)

    root_folder = sys.argv[1]
    batch_unzip_folders(root_folder)