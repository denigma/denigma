"""Manages the references of an article. 
Currently it creates the bibliography for a as "reStructured referenced"
marked article and and generated an rst file for it."""
import re

try:
   import article
except ImportError:
  print("No article module availble.")

try:
    import library
except ImportError:
   print("No library available.")


def referencing(self):
    print("Is article.")
    text = self.text.replace('\r', '').replace(r'\xe2\x80\x93', '-') # Second replace is probaly not any-more necessary.

    title_regex = "={2,}\n(.{2,})\n={2,}"
    title = re.findall(title_regex, text)
    if title: title = title[0]
    else: title = self.title
    #print title

    abstract_regex = "Abstract\n={8,}\n+(.+[\n\w\d\s.^!-~]+)\n+.+\n+={2,}"
    abstract = re.findall(abstract_regex, text)
    #print abstract

    references_regex = "References\n={10,}([.\n\w\d\s^!-~]{1,})\n{3}" #{366\xe2\x80\x93375}{\xe2\x80\x93}]{1,}"
    # Includes the "--" long dash non-asci character.
    references = re.findall(references_regex, text)[0].replace('*' , '') # Removes markup.
    #print references
    #print len(references), type(references)
    # for reference in references: print reference

    # Form a regular expression to fetch the main text part:

    #main_regex = "Abstract\n={8,}\n+.+[\n\w\d\s.^!-~]+\n+.+\n+={2,}([\n\w\d\s.^!-~]+)\n+References\n={10,}[.\n\w\d\s^!-~]{1,}\n{3}"#
    #main = re.findall(main_regex, text)
    # print "main is:", main

    def newSection():
        return section
        is_abstract = False

    #lines = text.split('\n')
    #for number, line in enumerate(lines):

        section = []
        if is_abstract:
            section.append(line)
        if line.startswith("Abstract"):
            section.append(line)
        if line.startwith('==='):
            lastline = section.pop[-1]
            Section('\n'.join(section))
            section = []
        elif line.startswith('---'):
            print("new subsection")
        elif line.startswith('~~~'):
            print("new subsubsection")
        elif line.startswith('^^^'):
            print("new subsubsubsection")
        elif line.startswith('References:'):
            print("Reference section starts")
        elif line.startwith('Table:'):
            print("new table")
        elif line.startwith('Figure:'):
            print("new figure")
        else:
            section.append(line)

    article.bibliography = library.Bibliography()

    a = article.Article()
    a.references = article.References(references, article=article) 

    text = text.encode('ascii', 'ignore')
    paragraph = article.Paragraph(text)
    a.paragraphs = [paragraph]
    a.referencing(numbered=True, brackets=False)
    # print a.string

    print("Outputing the document...")
    output = open('output.rst', 'w')
    output.write(a.string)
    output.close()

#23456789112345678921234567893123456789412346789512345678961234567897123456789  
