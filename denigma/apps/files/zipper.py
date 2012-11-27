"""Functions for zipping a file or an entire directory into a zipfile.
Inspired by:
http://peterlyons.com/problog/2009/04/zip-dir-python"""
import os
import zipfile


def zipIt(path, name):
    """Zips files"""    
    files = os.listdir(path)
    for f in files:
        with zipfile.ZipFile('microarray.zip', 'w') as zip_file:
            zip_file.write(f)

def zipdir(dirPath=None, zipFilePath=None, includeDirInZip=True):
    """Create a zip archive from a directory.

    Note that this funciton is designed to put files in the zip archive with
    either no parent directory or just one parent directory, so it will trim any
    leading directories in the filesystem paths and not include them inside the
    zip archive paths. This is generally the case when you want to just take a
    directory and make it into a zip file that can be extracted in different
    locations.

    Keyword arguments:

    dirPath -- string path to the directoy to archive. This the only
    required argument. It can be absolute or relative, but only one or zero
    leading directories will be included in the zip archive.

    zipFilePath -- string path to the output zip file. This can be absolute
    or relative path. If the zip file already exists, it will be updated. If
    not, it will be created. If you want to replace it from scratch, delete it
    prior to calling this function. (default is computed as dirPath + ".zip")

    includeDirInZip -- boolean indicting whether the top level directory should
    be inclued in the archive or omitted. (default True)


    Examples usages:
    
    zipdir("foo") # Just give it a dir and get a .zip file.
    zipdir("foo", "foo2.zip") # Get a .zip file with a specific file name
    zipdir("foo", "foo3dondir.zip", False) # Omit the top level directory.
    zipdir("../test1/foo", "foo4nopardirs.zip", False) # Exclude some leading dirs.
    zipdir("../test1/foo", "foo5pardir.zip") # Include some leading dirs.
    """
    if not zipFilePath:
        zipFilePath = dirPath + ".zip"
    if not os.path.isdir(dirPath):
        raise OSError("dirPath argument must point to a directory."
                      "'%s' does not." % dirPath)
    parentDir, dirToZip = os.path.split(dirPath)
    # Little nested fucntion to prepare the proper archive path:
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not includeDirInZip:
            archivePath = archivePath.replace(dirTOZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)

    outFile = zipfile.ZipFile(zipFilePath, "w",
                      compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dirPath):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
        # Make sure we get empty directories as well:
        if not fileNames and not dirNames:
            zipInfo = zipfiles.ZipInfo(trimPath(archiveDirPath) + "/")
            # Some web istes suggest doinf
            # zipInfo.external_attr = 16
            # or
            # zipInfor.external_attr = 48
            # Here to allow for inserting an empty directory. Still TBD/TODO.
            outFile.writestr(zipInfo, "")
    outFile.close()

if __name__ == "__main__":
    path = 'F:\\Documents\\Manuscripts\\DR-Essential\\MicroArray\\microarray'
    #zipIt(path, name='microarray.zip')
    zipdir(path)
