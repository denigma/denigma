"""Function to manage excel files."""
try: import xlrd
except: print("Failed to import xlrd to files.excel")


def dexcel(filename):
    """Dedexcels an Excel file."""
    import os
    print os.listdir('.')
    book = xlrd.open_workbook(filename)
    sheets = book.sheets()
    for sheet in sheets:
        output = open(filename.replace('xls', 'txt'), 'w')
        for i in xrange(sheet.nrows):
            output.write( '\t'.join( map(str, sheet.row_values(i) ) ) + '\n')
