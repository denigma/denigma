import os


def walking(dir_name, file_type):
    for path, dirs, files in os.walk(dir_name):
        print(path)
        print(dirs)
        print([f for f in files if f.endswith(file_type)])
        print '-' * 42

def log_files(dir_name, file_type):
    """Wraps os.walk in generator."""
    if not os.path.exists(dir_name):
        raise ValueError(dir_name + " not found!")
    if not os.path.isdir(dir_name):
        raise ValueError(dir_name + " is not a directory!")
    for path, dirs, files in os.walk(dir_name):
        log_files = [f for f in files if f.endswith(file_type)]
        for each_file in log_files:
            yield os.path.join(path, each_file)

def log_lines(dir_name, file_type):
    """Generator for each line of files."""
    for each_file in log_files(dir_name, file_type):
        for each_line in file(each_file).readlines():
            yield (each_file, each_line.strip())
            
def list_term(dir_name, file_type, term):
    """Filter out non-error lines."""
    return (each_file + ':' + each_line.strip()
            for each_file, each_line in log_lines(dir_name, file_type)
            if term in each_line.lower())

if __name__ == '__main__':
    dir_name = "F:/"
    file_type = '.py'
    #walking(dir_name, file_type)
##    for each_file in log_files(dir_name, file_type):
##        print(each_file)
##        print('')
    for each_error in list_term(dir_name, file_type, 'error'):
        print(each_error)
    
