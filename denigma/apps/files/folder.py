import os
import time

from afile import File


class Folder(dict):
    """A representation of a folder."""
    def __init__(self, path=None):
        dict.__init__(self)
        if path: self.path = path
        else: self.path = '.'
        self.update()
        self.downloads = []
        
    def update(self, path=None):
        """Updates its internal respresentation of the current folder state."""
        if not path:
            files = os.listdir(self.path)
        else: files = os.listdir(path)
        for f in files:
            lastmode_date = time.localtime(os.stat(os.path.join(self.path, f))[8])
            #print("Last modified data: %s" % lastmode_date)
            t = Time(time_object=lastmode_date)
            self[f] = File(f, self.path, t)
            
    def sort(self): 
        """Retrieve the file information form a selected folder.
        Sorts the files by last modified date/time and display in order newest file first."""   # http://www.daniweb.com/software-development/python/code/216688/file-list-by-date-python
        import os, glob, time
        #root = "D:\\d\\"    # One specific folder.
        #root = "D:\\d\\*"  # All the subfolders too.
        root = self.path

        date_file_list = []
        for folder in glob.glob(root):
            print "folder =", folder
            for file in glob.glob(folder + '/*.*'):
                stats = os.stat(file)   # Retrieves the stats for the current file as a tuple (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime). mtime (index8) is the last modfied date
                lastmod_date = time.localtime(stats[8])     # Create tuple (year yyyy, moth(1-12), day(1-31), hour(0-23), minute(0-59), second(0-59), weekday(0-6, 0 is monday), Julian day(1-366), dayligjt flag(-1.0 or 1)) from sedonds since epoch
                data_file_tuple = lastmod_date, file
                date_file_list.append(data_file_tuple)

        date_file_list.sort()
        date_file_list.reverse()    # newest mod date now first

        print "%-40s %s" % ("filename:", "last modified:")
        for file in date_file_list:
            folder, file_name = os.path.split(file[1])
            file_date = time.strftime("%m/%d/%y %H:%M:%S", file[0])
            print "%-40s %s" % (file_name, file_date)

        print('-'*60)
        date_name_list = []
        for file in date_file_list:
            folder, file_name = os.path.split(file[1])   # Extract just the filename.
            file_date = time.strftime("%m/%d/%y", file[0])
            date_name_list.append((file_date, file_name))
        date_count_dict = {}    # Contains date:count pairs.
        date_name_dict = {}     # Contains date:[files] pairs.
        for date, name in date_name_list:
            date_count_dict[date] = date_count_dict.get(date, 0) + 1
            date_name_dict.setdefault(date, []).append(name)
            
        import pprint
        print("Files with the same date:")
        pprint.pprint(date_name_dict)
        print('-'*60)
        print("Same dates count:")
        pprint.pprint(date_count_dict)

    def parse(self, rows=3):
        """Parses a specified number of rows of each file."""
        for f in self:
            print(">>> {0}:".format(f))
            if os.path.isfile(os.path.join(self[f].path, self[f].name)):
                self[f].parse(rows=rows)
            else:
                self.update(os.path.join(self.path,self[f].path))
                print("do something else")
            print('')
            

    def cleanUp(self, update=True):
        """Deletes all temporarily files which are not scripts .py nor serialisations (such as .pkl or .mrl)."""
        if update: self.update()
        for f in self:
            if not f.endswith('.py') and not f.endswith('.pkl') and not f.endswith('.mrl'):
                #os.remove(os.path.join(self[f].path, f))
                print("deleted "+f)
                
    def remove(self, filename, confirm=False):
        """Removes a file from the folder."""
        print "Removing:", os.path.join(self[filename].path, filename)
        if confirm:
            confirm = raw_input('Can you confirm? ')
            if confirm == "y":
                os.remove(os.path.join(self[filename].path, filename))
        else:
            os.remove(os.path.join(self[filename].path, filename))

    def startswith(self, string):
        """Returns all files which name starts with the given string."""
        result = []
        for f in self:
            if f.startswith(string):
                print("Found: %s" % f)
                result.append(self[f])
        return result

    def endswith(self, string):
        pass

    def contains(self, string):
        """Returns all files of which the name contains a given string."""
        result =[]
        for f in self:
            if string in f:
                result.append(self[f])
        return result

    def get(self, files):
        """Gets the files if they are not yet in the folder."""
        for f in files:
            f = File(f)
            self[f.name] = f


class Time():
    """A object representation of time point."""
    def __init__(self, year=None, month=None, week=None, day=None, hour=None, minute=None, second=None, week_day=None, year_day=None, is_dest=None, time_object=False):
        if time_object:
            year, month, day, hour, minute, second, week_day, year_day, is_dest = time_object.tm_year, time_object.tm_mon, time_object.tm_yday, time_object.tm_hour, time_object.tm_min, time_object.tm_sec, time_object.tm_wday, time_object.tm_yday, time_object.tm_isdst
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.week_day = week_day
        self.year_day = year_day
        self.is_dest = is_dest
    def __repr__(self):
        return "%s %s %s %s %s %s" % (self.year, self.month, self.day, self.hour, self.minute, self.second)
