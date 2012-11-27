"""Reads pdf documents."""
import os

import pyPdf
import slate


def getPDFContent(path):
    content = ''
    p = file(path, 'rb')
    pdf = pyPdf.PdfFileReader(p)
    num_pages = pdf.getNumPages()
    for i in xrange(0, num_pages):
        try:
            content += pdf.getPage(i).extractText() + '\n'
            print content
        except:
            pass # Over max page limit
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content

def main(filename, pypdf=False):
    if pypdf:    
        f = open(os.path.join('tests', 'test.txt'), 'w')
        parameter = 'xmlcharrefreplace'
        #parameter = "ignore"
        pdfl = getPDFContent(filename).encode("ascii", parameter)
        f.write(pdfl)
        f.close()
    else:
        print filename
        with open(filename) as f:
            doc = slate.PDF(f)
            
        return doc

if __name__ == '__main__':
    path = "F:/Literature/DR"
    filename = "mTORC1 in the Paneth cell niche couples intestinal stem-cell function to calorie intake"
    pdf = main(os.path.join(path, filename+".pdf"))


    
