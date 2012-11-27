import os
import urllib

from extraction import extract


class File(): # Extend its capabilities with those of build-in file
    """Mirrors a file object, its name, location and create/update date"""
    def __init__(self, name=None, path='.', date=None, size=None, url=None):
        if name and name.startswith('http:'): # A url is given as name to download.
            self.url = url = name
            self.name = name.split('/')[-1]
            print "name=", self.name, url
        elif name:
            self.name = name or None
        elif not name and url:
            self.name = url.split('/')[-1]
        self.path = path
        self.date = date
        self.size = size
        
        if url:
            if url[-4] == "." or url[-3] == ".": #in url.split('/')[-1]:
                self.url = "/".join(url.split('/')[:-1])
                print "url=", self.url
            else:
                self.url = url
            self.retrieve(self.path)
        else:
            self.url = url
        self.x = 0          # For iterator.
        #self.delimiter = delimiter
        #super(File, self).__init__()
        
    def __repr__(self):
        return '\t'.join(map(str, [self.name, self.date, self.path]))

    def __str__(self):
        return self.__repr__
    
    def parse(self, rows=False, memory=False, seperator='\t', delimiter='\n', header=False, printing=False, term=False, list=True, ignore=0):
        """Parses the file an prints the rows out.
        Make an iterator out of it!"""
        if memory:
            if self.path != '.':
                f = file(os.path.join(self.path, self.name)).read().split(delimiter)   # open , 'r'
            else:
                f = file(self.name).read().split(delimiter)
        else:
            import fileinput
            if self.path != '.':
                f = fileinput.input([os.path.join(self.path, self.name)])
            else:
                print os.listdir('.')
                f = fileinput.input([self.name])
        line_count = 0
        if header:
            if isinstance(header, bool):    # Automatically generated header.
                headers = {}
            else:                           # Customized header.
                headers = dict(zip(range(len(header)), header))
        if ignore: start = ignore+1
        else: start = 0
        contents = []
        for line in f:          # xrange(0, len(f)):
            #print line
            if not line.strip():
                print "Empty line:", line, line_count
                line_count += 1
                continue
            if ignore and line_count <= ignore:
                line_count += 1
                continue
            #if line.strip() == "": continue
            if not line:
                line_count += 1
                continue
            if line.endswith('\r'): line = line[:-1]
            if line.endswith('\n'): line = line[:-1]
            if term and term in line: printing = True
            if printing: print line             # f[x]
            if header:
                fields = line.split(seperator)           # f[x].split('\t')
                D = {}
                for y in xrange(0, len(fields)):
                    if line_count == 0 or line_count == start:            # x == 0:
                        if isinstance(header, bool):
                            headers[y] = fields[y]
                        continue
                    try:
                        D[headers[y]] = fields[y]
                    except KeyError: continue  # more coloumns in field as columns defined in header will be ignored.
                #if line.startswith('#'): continue
                #if D:
                contents.append(D)
            else:
                if seperator:
                    fields = line.split(seperator)
                else:
                    fields = line
                contents.append(fields)
            line_count += 1
            if line_count == rows: break
        try: f.close()
        except AttributeError:
            #print f
            pass # memory read file need not to be closed.
        #if printingprint
        if header: contents = contents[1:] # Omit the header line which resulted in an empty line.
        return contents

    def retrieve(self, folder='.'):
        print self.url, self.name, folder
        print("Downloading from %s to %s" % (os.path.join(self.url, self.name), os.path.join(folder, self.name)))
        response = urllib.urlretrieve(self.url+'/'+self.name, os.path.join(folder, self.name))
        print(self.name)
        if self.name.endswith('.gz') or self.name.endswith('.zip'):
            #upzipFile(f)
            self.extract(folder=folder)

    def get_context(self):
        """Gets the context of the file."""
        self.contents = self.parse(memory=True, list=True, printing=False)

    def __iter__(self):
        self.get_context()
        return self

    def next(self):
        self.x += 1
        if self.x >= len(self.contents):
            raise StopIteration
        return self.contents[self.x]

    def __len__(self):
        if not hasattr(self, 'contents'):
            self.get_context()
        return len(self.contents)
  
    def extract(self, folder='.'):
        self.name = extract(self.name, self.path)
        print("Filename of extracted file is %s" % self.name)
##        """Is intended to detect file archive type and use appropriate extraction methodology.
##        Should be flexible in working with coming archive formats, such as tar.gz, rar and zip."""
##        if self.name.endswith('.tar.gz'):    # http://code.activestate.com/recipes/442503-extracting-targz-files-in-windows/
##            print "file endswith .tar.gz"
##            import tarfile
##            try:
##                tar = tarfile.open(self.name, 'r:gz')
##                for item in tar:
##                    tar.extract(item)
##                #os.remove(os.path.join(folder, self.name))
##                print "delete", os.path.join(folder, self.name)
##                print "Done"
##            except:
##                name = os.path.basename(self.name)
##                print name[:name.rfind('.')], '<filename>'
##        elif self.name.endswith('.zip'):
##            import zipfile
##            #fh = open(filename, 'rb')
##            #print self.name, folder, os.path.join(folder, self.name)
##            z = zipfile.ZipFile(os.path.join(folder, self.name))
##            for name in z.namelist():
##                if name.endswith('/'):
##                    try: os.makedirs(name)
##                    except WindowsError: print f, 'already exists.'
##                z.extract(name, folder)
##                print "extracted", name
##            z.close()
##            #os.remove(os.path.join(folder, self.name))
##            print "deleted", self.name

    def delete(self):
        """Deletes itself."""
        os.remove(os.path.join(self.path, self.name))


    
