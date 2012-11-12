"""Provides template tags to generate and process tables
in data entry text (i.e. article content)."""
import re

from django import template


register = template.Library()

@register.filter
def tables(text):
    """
    Generates rst tables from raw data.

    The recommended format for raw table is::

        Table: Title
        ------------
        Legend
        Header
        Data
    """
    global number
    number = 1
    table_names = {}
    #print text
    #regex = re.compile(".. table::(?P<title>[\w\d]+)\n(?P<legend>[\w\d]+)\n(?P<data>)[\w\d]+\n\n]")
    #regex = re.compile("Table\n\W{5}](.+)\n\n", re.DOTALL)
    #rc = re.compile("Table: (?P<title>\w+)\n\W{5,100}(?P<legend>.+?)\n(?P<data>.+)\n\n", re.DOTALL)
    rc = re.compile("#* {0,1}(?P<pre>\.\. table\:\: \*\*){0,1}Table: (?P<title>[*,.)(/\w \d-]+)\.{0,1}\n\W*(?P<legend>[\/;\*\,\(\).\-_,+=\w\s\d]+?\.\n){0,1}(?P<data>.+?)[\n]{2}?", re.DOTALL)
    def translate(match): # Terms that are up-regulated in the liver_ by lipoic acid treatment in young rats
        #print("Object: %s" % match)
        #print("Match: %s" % match.group(0))
        #print("Title: %s" % match.group('title'))
        #print("Legend: %s" % match.group('legend'))
        #print("Data: %s" % match.group('data'))
        #print locals(), "number" in globals()

        number = globals()['number']

        if not match.group('title').endswith('.**'):
            table_names['Table: %s' % match.group('title')] = 'Table %s' % number
            table = create_table(match.group('data'), match.group('title'), match.group('legend'), number)
        else:
            table_name =  match.group('title').replace('.**', '')
            table_names['Table: %s' % table_name] = 'Table %s' % number
            #table = "%s\n\n    %s" % (match.group('title'), match.group('data'))
            table =  match.group(0).replace("Table: ", "Table %s: " % number) # + '\n\n.. _`Table %s`:' % number
            #print table
        #print  globals()['number'],match.group('title'), match.group(0)
        table_link = '.. _`Table %s`:\n' % number
        globals()['number'] += 1
        #print(table_link + table)
        return table_link + table

    text = rc.sub(translate, text.replace('\r', '')+'\n\n')
    for table_name, table_number in table_names.items():
        text = text.replace(table_name, "`%s`_" % table_number)

    #print text
    return text+'\n.. fin\n'

def create_table(data, title=None, legend=None, number=1, intend=" "*4):
    # Determine max row length of each column
    #table_dict[row_number] = columns
    row_length = {}
    rows = data.split('\n')
    #print(rows)
    if not title and not legend:
        title  = rows[0]
        legend = rows[1]
        header = rows[2].split('\t')
        rows = rows[3:]
    elif not legend:
        #print("No legend")
        legend = ''
        header = rows[0].split('\t')
        rows = rows[1:]
    else:
        header = rows[0].split('\t')
        rows = rows[1:]

    for index, head in enumerate(header):
        row_length[index] = len(head)
    for row in rows:
        columns = row.split('\t')
        for index, column in enumerate(columns):
            if len(column) > row_length[index]:
                row_length[index] = len(column)

    table_construct = []

    table_row = []
    for i in xrange(len(header)):
        table_row.append('='*row_length[i])
    table_construct.append(intend+"  ".join(table_row))

    table_row = []
    for index, head in enumerate(header):
        table_row.append(head.ljust(row_length[index]))
    table_construct.append(intend+"  ".join(table_row))

    table_row = []
    for i in xrange(len(header)):
        table_row.append('='*row_length[i])
    table_construct.append(intend+"  ".join(table_row))

    for row in rows:
        #print row
        table_row = []
        columns = row.split('\t')
        for index, column in enumerate(columns):
            table_row.append(column.ljust(row_length[index]))
        table_construct.append(intend+"  ".join(table_row))

    table_row = []
    for i in xrange(len(header)):
        table_row.append('='*row_length[i])
    table_construct.append(intend+"  ".join(table_row))

    return ".. table:: **Table %s: %s**. %s\n\n%s\n\n----\n\n" % (number, title, legend, "\n".join(table_construct))

def create_table_t1():
    table = """Test table.
This is a text table.
type\tvalue\ttested
foo\t1\tTrue
bar\t2\tFalse"""
    print(table)
    print("")
    rst_table = create_table(table)
    print(rst_table)

def create_table_t2():
    title = "Test table."
    legend = "This is a text table."
    table = """type\tvalue\ttested
foo\t1\tTrue
bar\t2\tFalse"""
    print(table)
    print("")
    rst_table = create_table(table, title, legend)
    print(rst_table)

def tables_t():
    table = """Table: Test table
-----------------
This is a text table.
type\tvalue\ttested
foo\t1\tTrue
bar\t2\tFalse

"""
    print tables(table)

    #string = """Table: Test table\n-----------\nThis is the test table Legend.\nadsat\tdfs\ta\ndsf dsad\n\nsdaasd \n"""
    #print tables(string)

if __name__ == '__main__':
    #create_table_t2()
    tables_t()

