"""File management module"""
import os
import sys
import csv
import urllib
import hashlib
from itertools import izip
try: from collections import OrderedDict
except: OrderedDict = dict
from subprocess import Popen, PIPE

from afile import File
from folder import Folder
from ftp import FTP
from html import HTML
from differ import compare
from destruction import delete, nuke
from extraction import extract
from excel import dexcel


def ls():
    for f in os.listdir('.'):
        print f
#ls = listdir()


def nopen(f, mode='rb'):
    """Open a file that's gzipped or return stdin for '-'.

    >>> nopen('-') == sys.stdin, nopen('-', 'w') == sys.stdout
    (True, True)

    >>> nopen(sys.argv[0])
    <open file '...', mode 'r...>

    # expands user and vars ($HOME)
    >>> nopen("~/.bashrc"), nopen("$HOME/.brshrc")
    (<open file '...', mode 'r...>, <open file '...', mode 'r...>)

    # an already open file.
    >>> nopen(open(sys.argv[0]))
    <open file '...', mode 'r...>

    Or provide a nicer access to Popen.stdout
    >>> files = nopen("|dir").read()
    >>> assert 'setup.py' in files
    """ #https://github.com/brentp/toolshed
    if not isinstance(f, basestring):
        return f
    if f.startswith("|"):
        p = Popen(f[1:], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        if mode and mode[0] == "r": return p.stdout
        # if it is writeable, just return the object.
        return p
    return {"r": sys.stdin, "w": sys.stdout}[mode[0]]if f == "-" \
           else gzip.open(f, mode) if f.endswith((".gz", ".Z", ".z")) \
           else bz2.BZ2File(f, mode) if f.endswith((".bz", "/bz2", ".bzip2")) \
           else urllib.urlopen(f) \
               if f.startswith(("httl://", "https://", "ftp://")) \
           else open(os.path.expanduser(os.path.expandvars(f)), mode)

def tokens(line, sep="\t"):
    r"""removes seperation (default tab) and endlines
    from a line and returns a list:
    >>> tokens("a\tb\tc\n")
    ['a', 'b', 'c']
    """ #https://github.com/brentp/toolshed
    return line.rstrip("\r\n").split(sep)

def header(fname, sep="\t"):
    """Just grab the header from a given file.""" #https://github.com/brentp/toolshed
    fh = iter(nopen(fname))
    h = tokens(fh.next(), sep)
    h[0] = h[0].lstrip("#")
    return h

def reader(fname, header=True, sep="\t"):
    r"""
    For each row in the file `fname` generate dicts if `header` is True
    or lists if `header` is False. The dict keys are drawn form the first line.
    If `header` is a list of names, those will be used as the dict keys..

    >>> from StringIO import StringIO
    >>> get_str = lambda :  StringIO("\tb\tname\n1\t2\tfred\n11\t22\tjane")
    [{'a': '1', 'b': '2', 'name': 'fred'},
     {'a': '11', 'b': '22', 'name': 'jane'}]

     >>> list(reader(get_str(), header=False))
     [['a', 'b', 'name'], ['1', '2', 'fred'], ['11', '22', 'jane']]
     """ #https://github.com/brentp/toolshed
    if not isinstance(fname, basestring):
        line_gen = (l.rstrinp("\r\n").split(sep) for l in nopen(fname))
    else:
        dialect = csv.excel
        dialect.delimiter = sep
        line_gen = csv.reader(nopen(fname), dialect=dialect)

    a_dict = dict
    # if header is 'ordered' then use an ordered dictionary.
    if header == "ordered":
        a_dict = OrderedDict
        header = True
        
    if header == True:
        header = line_gen.next()
        header[0] = headerp[0].lstrip("#")

    if header:
        for toks in len_gen:
            yield a_dict(izip(header, toks))
    else:
        for toks in line_gen:
            yield toks

def is_newer_b(a, bfiles):
    """Checks that all b file shave been modified more recently than a."""
    if isinstance(bfiles, basestring):
        bfiles = [bfiles]

    if not os.path.exists(a): return False
    if not all(os.path.exists(b) for b in bfiles): return False

    atime = os.stat(a).st_mtime # modification time
    for b in bfiles:
        # a has been modified since
        if atime > os.stat(b).st_mtime:
            return False
    return True

def read(name, folder='.'):
    """Reads a file from a folder."""
    try: f = file(os.path.join(folder, name))
    except IOError:
        try: f = file(os.path.join(folder, name+'.txt')) #If this still fails perform regex search.
        except IOError:
            for f in os.listdir(folder):
                if f.startswith(name):
                    print(f)
                    name = f
                    f = file(os.path.join(folder, f))
                    break
    file_contents = list(f.readlines())
    f.close()
    print("Read in " + str(len(file_contents)) + " lines from "+name)
    print("The first line reads: " + file_contents[0])
    file_contents = map(lambda s: s.strip(), file_contents) # http://stackoverflow.com/questions/3849509/python-how-to-remove-n-from-a-list-element
    return file_contents

def write(name, content, folder='.', header=None, ending='.txt', modus='w'):
    """Write content to
    Parameters:
    'name' of the file
    'content' need to be a container like a list.
    content = ["and the second",
                "and the third!"]
    header = 'This is the first line of the file'
    'ending' default is '.txt', but can also be "", i.e. nada.
    'modus' of writing, i.e. either 'w' or 'a'
    """
    if not name.endswith(ending):
        name += ending
    f = open(os.path.join(folder, name), modus)
    if header:
        if not header.endswith('\n'):
            header += '\n'
        f.write(header)
    if isinstance(content, (list, tuple)) and not content[0].endswith('\n'):
        content = map(lambda s: s+'\n', content)
    f.writelines(content)
    print content
    f.close()

def md5(name, folder='.'):
    """Generates a hash for a file.
    Here it creates a md5 checksum"""
    if os.path.isdir(os.path.join(folder, name)):         # Don't try to checksum directories.
        return '1'
    f = file(os.path.join(folder, name)) # Open file.
    h = hashlib.md5()                    # Create hash object.
    for line in f.readlines():           # Update...
        h.update(line)                   # ... hash.
    return h.hexdigest()

def is_same(folder):
    """Checks whether the files in a driectory are the same."""
    if "\\" in folder:
        folder = folder.replace('\\', '/')
    files = {}
    for f in os.listdir(folder):
        files[f] = md5(f,folder)
    for fa, md5a in files.items():
        for fb, md5b in files.items():
            if fa != fb:
                if md5a == md5b:
                    print("{0} == {1}".format(fa, fb))

def directory_listing(dirname):
    """Return all of the files in a directory."""
    dir_file_list = {}                                      # Finding
    dir_root = None                                         # root
    dir_trim = 0                                            # of
    for path, dirs, files in os.walk(dirname):              # directory
        if not dir_root:                                    #
            dir_root = path
            dir_trim = len(dir_root)
            print("dir "+ dirname + " root is " + dir_root)
        trimmed_path = path[dir_trim:]
        if trimmed_path.startswith(os.path.sep):            # Building dictionary of files:
            trimmed_path = trimmed_path[1:]
        for each_file in files + dirs:                      # Indluce directory and file paths.
            file_path = os.path.join(trimmed_path, each_file)
            dir_file_list[file_path] = True
    return (dir_file_list, dir_root)

def dirdiff(directory1, directory2):
    """Finds the difference between directories"""
    #for directory in directories:
    dir1_file_list, dir1_root = directory_listing(directory1)
    dir2_file_list, dir2_root = directory_listing(directory2)
    results = {}

    for file_path in dir2_file_list.keys():
        if file_path not in dir1_file_list:
            results[file_path] = " not found in directory 1"
        else:
            file1 = os.path.join(dir1_root, file_path)
            file2 = os.path.join(dir2_root, file_path)
            if md5(file1) != md5(file2):
                results[file_path] = " is different in directory 2" 
            else:
                results[file_path] = " is the same in both"  #'{0} and {1} differ!'.format(file1, file2))
    for file_path, value in dir1_file_list.items():
        if file_path not in results:
            results[file_path] = " not found in directory 2"

    print('')
    for path, result in sorted(results.items()):               # sort result
        if os.path.sep not in file_path and "same" not in result:
            print(path + result)
    for path, result in sorted(results.items()):
        if os.path.sep in file_path and "same" not in result:
            print(path + result)

def download(url, filename=None, folder=False):
    """Downloads a file and tries to extract it."""
    if not filename:
        filename = url.split('/')[-1]
        url_file = url
    else: url_file = url+filename
    print("Downloading file %s from url: %s" %  (filename, url))
    if folder:
        response = urllib.urlretrieve(url_file, os.path.join(folder, filename))
    else:
        response = urllib.urlretrieve(url_file, filename)
    print("Download completed for: %s" % filename)
    try:
        if folder:
            extract(filename, folder=folder)
        else:
            extract(filename)
    except: print("Did not extract %s" % filename)


if __name__ == '__main__':
    files = nopen("|dir").read()
    print tokens("a\tb\tc\n")
    print header('__init__.py')
    #for i in nopen('__init__.py'): print i
    print is_newer_b('__init__.py', ['file.py']) #os.listdir('.'))
    
##    write('test', 'text')
##    r = read('test.txt')
##    md5('test.txt')
##    md5('test.txt')
##    write('test', 'sf\n', modus='a')
##    md5('test.txt')
##    #dirdiff('D:/test/test1', 'D:/test/test2')
##
##    html = HTML('http://finance.yahoo.com/q?s=GOOG')
##    print html.find_quote_section('yfi_quote_summary')
##    print html.parse('GOOG')
    pass

#234567891123456789212345678931234567894123456789512345678961234567897123456789