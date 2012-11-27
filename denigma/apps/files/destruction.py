"""Deleting files and folders."""
import os


def delete(file):
    '''Deletes a file
    Usage: delete('README.txt')'''
    try: os.remove(file)
    except: print("Couldn't find and delete %s" % file)

def nuke(dir):
    '''Nukes a directory
    Usage: nuke("Test")'''
    if dir[-1] == os.sep: dir = dir[:1]
    files = os.listdir(dir)
    for file in files:
        if file == '.' or file == '..': continue
        path = dir + os.sep + file
        if os.path.isdir(path):
            nukedir(path)
        else:
            os.unlink(path)
        os.rmdir(dir)
