"""Compares to files line by line and identifies the differences."""
#import difflib


def stringComp(string1="abcdefghijklmnop", string2="abcdefghi"):
    if len(string1.split(string2)) > 0:
        if string1 == string1.split(string2)[0]:
            finalstring = stringComp(string2, string1)
        else:
            finalstring = ''.join(string1.split(string2))
    else:
        finalstring = ''
    return finalstring
#print stringComp()

def compare(file1, file2):
    input1 = file(file1).read().split('\n')
    input2 = file(file2).read().split('\n')
    for x in xrange(0, len(input1)):
        if input1[x].strip(' ') != input2[x].strip(' '):
            
           # print x+1, ':'#, #input1[x], '|', input2[x]
            d1 = ''
            d2 = ''
            if len(input1[x]) < len(input2[x]): length = len(input1[x])
            else: length = len(input2[x])
            for y in xrange(length-1):
                if input1[x][y] != input2[x][y]:
                    try: d1 += input1[x][y]
                    except: pass
                    try: d2 += input2[x][y]
                    except: pass
            #print y, '\t%s | %s' % (d1, d2)
                    
            #print x+1, ':', y, '\t%s' % d1
            #print x+1, ':', y, '\t%s' % d2

            print x+1, ':', input1[x]
            print x+1, ':', input2[x]
            print
            
            #except: print length, len(input1[x]), len(input2[x]), y
            #print "".join(input1[x].split(input2[x]) if len(input1[x]) > len(input2[x]) else input2[x].split(input1[x]))

            #s = difflib.SequenceMatcher(input1[x], input2[x])
            #for block in s.get_matching_blocks():
            #    print "match of length %d at a[%d] and b[%d]" % block
            #stringComp(input1[x].strip(' ') , input2[x].strip(' ') )

if __name__ == '__main__':
    #compare('test.py', 'testDataManager.py')
    compare(r'D:\gl\flyinghigh2\test\bestiary.py',
            r'D:\gl\flyinghigh2\test\bestiary1.py')
    
