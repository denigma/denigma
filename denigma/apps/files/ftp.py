"""A FTP connection management class."""
import os
import urllib

from afile import File
from extraction import extract


class FTP(dict):
    """A ftp site harbours files.

    Specify a url and it will be inspected for available files.
    If path is given downloaded files will be saved their.
    Specified files can be retrieved
    or all files can be downloaded.

    Usage:
    from files import FTP
    FTP('ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/',
        path='./gene/DATA/').retrieve('gene_history.gz')

    """
    def __init__(self, url, path=None):
        dict.__init__(self)
        self.url = url
        if path: self.path = path
        else: self.path = '.'
        print("URL contents:")
        self.downloads = []
        self.extracted = []
        for f in urllib.urlopen(url).read().split('\r\n'):
            print(f)
            if f == '': continue # Ignore empty line.
            f = f.split()
            date = f[5:8]
            name = f[-1]
            if name[:3] == '../': continue # Ignore "parent dictory" link.
            f = File(name, url, date)
            self[name] = f
            
    def retrieve(self, files):
        """Retrieves specified file(s)."""
        if isinstance(files, str):
            files = [files]
        for name in files:
            for f in self:
                if f.startswith(name):
                    print self.url+'/'+f, f
                    response = urllib.urlretrieve(self.url+'/'+f, os.path.join(self.path, f))
                    print("+ {0} retrieved".format(f))
                    if f.endswith('.gz'):
                        files = extract(f, folder=self.path)             # upzipFile(f)
                        if isinstance(files, list):
                            self.extracted.extend(files)
                        else:
                            self.extracted.append(files)
                        extracted = f[:-3]
                        print("+ {0} extracted".format(extracted))
                        print("- {0} deleted".format(f))
                        f = extracted
                    self.downloads.append(f)

    def download(self):
        """Downloads all files from ftp server."""
        print("Downloading:")
        for f in self:
            self.retrieve(f)

    def remove(self, confirm=False):
        """Removes the downloaded files from the harddisc."""
        for f in self.downloads:
            print("Removing %s from %s" % (f, self.path))
            if confirm:
                confirming = raw_input("Confirming? ")
                if confirming == "y":
                    if self.path == '.':
                        os.remove(f)
                    else:
                        os.remove(os.path.join(self.path, f))
            else:
                if self.path == '.':
                    os.remove(f)
                else:
                    os.remove(os.path.join(self.path, f))
                    
        for f in self.extracted:
            os.remove(os.path.join(self.path, f))
            
