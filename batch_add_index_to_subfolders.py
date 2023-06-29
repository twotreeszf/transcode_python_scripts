# encoding: utf-8
import os
from os import path
import sys

def batch_add_index_to_subfolders(root_folder):
    folders = [f for f in os.listdir(root_folder) if path.isdir(path.join(root_folder, f))]
    i = 1
    for folder in folders:
        org_path = path.join(root_folder, folder)
        new_path = path.join(root_folder, '{:03d}-'.format(i) + folder)

        os.rename(org_path, new_path)
        i+=1

if __name__ == '__main__':

    if len(sys.argv) < 2:
        message = '''
                Usage:
                python batch_add_index_to_subfolders.py [root_folder]
                '''
        print(message)
        exit(1)

    root_folder = sys.argv[1]
    batch_add_index_to_subfolders(root_folder)