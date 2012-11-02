#! -.- coding: utf8 -.-
"""Manages the references of an article.
Currently it creates the bibliography for a as "reStructured referenced"
marked article and and generated an rst file for it."""
import os
import re

from django.conf import settings

try:
   import article as a
except ImportError as e:
  print("No article module available. %s" % e)

try:
    import denigma.library as library #denigma.library as
except ImportError:
   print("No library available.")


def referencing(self):
    print("Is article.")
    if isinstance(self, (str, unicode)):
        text = self.replace('\r', '').replace(r'\xe2\x80\x93', '-') # Second replace is probaly not any-more necessary.
    else:
        text = self.text.replace('\r', '').replace(r'\xe2\x80\x93', '-') # Second replace is probaly not any-more necessary.
    text = text.encode('ascii', 'ignore')
    article = a.Article()

    title_regex = "={2,}\n(.{2,})\n={2,}"
    title = re.findall(title_regex, text)
    if title: title = title[0]
    else: title = self.title
    #print title

    #article.title = title

    abstract_regex = "Abstract\n={8,}\n+(.+[\n\w\d\s.^!-~]+)\n+.+\n+={2,}"
    abstract = re.findall(abstract_regex, text)
    #print abstract


    references_regex = "References\n={10,}([.\n\w\d\s^!-~]{1,})\n{3}" #{366\xe2\x80\x93375}{\xe2\x80\x93}]{1,}"
    # Includes the "--" long dash non-asci character.
    references_regex = re.compile("References\n\W{10}(.+?)\n{3}", re.DOTALL)
    references = re.findall(references_regex, text)[0].replace('*' , '') # Removes markup.
    #print references.split('\n')[:50]
    #print len(references)#, type(references)
    # for reference in references: print reference

    # Form a regular expression to fetch the main text part:

    #main_regex = "Abstract\n={8,}\n+.+[\n\w\d\s.^!-~]+\n+.+\n+={2,}([\n\w\d\s.^!-~]+)\n+References\n={10,}[.\n\w\d\s^!-~]{1,}\n{3}"#
    #main = re.findall(main_regex, text)
    # print "main is:", main


    article.bibliography = library.Bibliography()
    print references
    #stop

    article.references = a.References(references, article=article)

   #section_headers = re.findall('\n([\w -:.,/]+)\n={3,}', text)    
   #subsections_headers = re.findall('\n([\w -:.,/]+)\n-{3,}', text) 
   #subsubsections_headers = re.findall('\n([\w -:.,/]+)\n~{3,}', text) 
   #subsubsubsections_headers = re.findall('\n([\w -:.,/]+)\n^{3,}', text) 
   #table_headers = re.findall('\nTable: ([\w -:.,/]+)\n-{3,}', text)

    def newSection(section, level):
        print("New %s: %s:" % (level, latest_line))
        print "contains %s lines" % len(section)
        section = a.Section(title=latest_line)
        if "abstract" == level:
           section.title = "Abstract"
        #elif "subsub" in level:
        #   article.section.subsections.append(section)
        elif "sub" in level:
          # if isinstance(section, a.Subsection):
           #   article.section[-1].subsections[-1].subsections.append(section)
           article.sections[-1].subsections.append(section)
        else:
           article.sections.append(section)
        article.section = section
        print section.title
        #section = [] # New section
        return section

    if False:
      stop
      section = []
      type = False
      ignore = False 
   
      #print("Parsing article text")
      lines = text.split('\n')
      for number, line in enumerate(lines):
        #print line[:50]
        if ignore == number: continue
        if line.startswith("Abstract"):
            type = 'abstract'
            article.abstract = a.Abstract()
            article.abstract.text = []
            section.append(line)
            ignore = number + 1
            section = a.Section(title=latest_line)
            #section = newSection(section, 'section')

        elif line.startswith('==='):
            if type == 'abstract':
                article.abstract.text.pop() # =====
                lastline = article.abstract.text.pop()
                print "Lastline is:", lastline
                article.abstract.text = '\n'.join(article.abstract.text)
                type = False

                section = newSection(section, 'abstract')
            else:
               section = newSection(section, 'section')


        elif line.startswith('---'):
            section = newSection(section, 'subsection')

        elif line.startswith('~~~'):
            section = newSection(section, 'subsubsection')

        elif line.startswith('^^^'):
            section = newSection(section, 'subsubsubsection')

        elif line.startswith('References:'):
            print("Reference section starts %s:" % latest_line)
            #lastline = section.pop()
            section = a.Section(title=latest_line)
            section.text = []
        elif line.startswith('Table:'):
            print("new table %s:" % latest_line)
            #lastline = section.pop()
            section = a.Section(title=latest_line)
            section.text = []
        elif line.startswith('Figure:'):
            print("new figure %s:" % latest_line)
            #lastline = section.pop()
            section = a.Section(title=latest_line)
            section.text = []
        elif type == 'abstract':
            article.abstract.text.append(line)
        else:
            section.append(line)
            print line[:50]
        latest_line = line
        if hasattr(section, 'paragraphs'):
           if line:
              section.paragraphs.append(a.Paragraph(line))

            #Section('\n'.join(section))
            #section = []
      print "\nSummary:"
      print "Title:", article.title
      print "Abstract:", len(article.abstract.text)
      print "Sections:", len(article.sections)
      for section in article.sections:
        print section.title, len(section.subsections)
        for subsection in section.subsections:
            print " %s" % subsection.title, len(subsection.paragraphs)
            for subsubsection in subsection.subsections:
                print "  %s" % subsection.title, len(subsection.paragraphs)

    #print article.abstract.text

    def translate(match):
        return ''
    rc = re.compile(references_regex)
    text = rc.sub(translate, text)
    from articles.templatetags.tabling import tables
    from articles.templatetags.math import formula
    from lifespan.templatetags.factor_linker import symbols
    paragraph = a.Paragraph(tables(symbols(formula(text, uni=False))).replace('.. header: ', '.. header:: '))
    article.paragraphs = [paragraph]
    article.referencing(numbered=True, brackets=False)
    # print a.string

    print("Outputing the document...")
    output = open(os.path.join(settings.PROJECT_ROOT, 'output.rst'), 'w')
    output.write(article.string)
    output.close()
    return article.string

#23456789112345678921234567893123456789412346789512345678961234567897123456789  
