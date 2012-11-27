"""Extracts files and folders."""
import os


def extract(filename, folder='.'):
    """Is intended to detect file archive type and use appropriate extraction methodology.
    Should be flexible in working with coming archive formats, such as tar.gz, rar and zip."""
    files = []
    if filename.endswith('.tar.gz'):    # http://code.activestate.com/recipes/442503-extracting-targz-files-in-windows/
        import tarfile
        try:
            tar = tarfile.open(filename, 'r:gz')
            for item in tar:
                tar.extract(item)
                files.append(item)
            #os.remove(os.path.join(folder, filename))
            print "Done"
            tar.close()
        except Exception as e:
            print "Exception occurred by extracting:", e
            name = os.path.basename(filename)
            print name[:name.rfind('.')], '<filename>'
        os.remove(os.path.join(folder, filename))
        filename = filename[:-8]

    elif filename.endswith('.gz'): # http://docs.python.org/library/gzip.html
        import gzip
        
        f = gzip.open(os.path.join(folder, filename), 'rb')
        file_content = f.read()
        f.close()
        output = open(os.path.join(folder, filename[:-3]), 'w')
        output.writelines(file_content)
        output.close()
        os.remove(os.path.join(folder, filename))
        filename = filename[:-3]

##        fileObj = gzip.GzipFile(filename, 'rb')
##        fileObjOut = file(os.path.join(folder, filename).replace('.gz', ''), 'wb')
##        while 1:
##            lines = fileObj.readline()
##            if not lines: break
##            fileObjOut.write(lines)
##        fileObj.close()
##        fileObjOut.close()
        
    elif filename.endswith('.zip'):
        import zipfile
        #fh = open(filename, 'rb')
        print("Trying to extract zip: %s %s %s" % (filename, folder, os.path.join(folder, filename)))
        z = zipfile.ZipFile(os.path.join(folder, filename))
        for name in z.namelist():
            print("%s is in archive." % name)
            if name.endswith('/'):
                try: os.makedirs(name)
                except WindowsError: print name, 'already exists.'
            z.extract(name, folder)
            print("Extract %s from %s." % (name, folder))
        z.close()
        os.remove(os.path.join(folder, filename))
        filename = name#filename[:-4]
    return files or filename
